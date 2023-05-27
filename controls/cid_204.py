import boto3
import csv
import os

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure AWS EBS Volume snapshots are encrypted with KMS using a customer managed Key (CMK)"

def control(kms_client, key_arn):
    key_manager, evidence = "", ""
    response = kms_client.describe_key(
        KeyId=key_arn
    )

    key_manager = response["KeyMetadata"]["KeyManager"]
    evidence = f"['Key ID': '{key_arn}']['KeyManager': '{key_manager}']"
    return key_manager, evidence

def main():
    print(CONTROL_DESCRIPTION)

    with open('/tmp/cid_204_controls.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Count", "Snapshot ID", "Region", "Result", "Evidence"])
        count = 1

        for region in REGIONS:
            ec2_client = boto3.client('ec2', region)
            kms_client = boto3.client('kms', region)

            try:
                response = ec2_client.describe_snapshots(
                    Filters=[
                        {
                            'Name': 'owner-id',
                            'Values': [boto3.client('sts').get_caller_identity().get('Account')],
                        },
                    ],
                    MaxResults=200
                )

                snapshots = response["Snapshots"]

                while "NextToken" in response:
                    response = ec2_client.describe_snapshots(
                        NextToken=response["NextToken"],
                        Filters=[
                            {
                                'Name': 'owner-id',
                                'Values': [boto3.client('sts').get_caller_identity().get('Account')],
                            },
                        ],
                        MaxResults=200
                    )
                    snapshots.extend(response["Snapshots"])

                for snapshot in snapshots:
                    snapshot_id = snapshot["SnapshotId"]
                    encrypted = snapshot["Encrypted"]

                    if not encrypted:
                        row = [f"{count}", f"{snapshot_id}", f"{region}", "FAIL", "['Encrypted': False]"]
                        csv_writer.writerow(row)
                    else:
                        kms_id = snapshot["KmsKeyId"]
                        key_manager, evidence = control(kms_client, kms_id)

                        if key_manager == "AWS":
                            row = [f"{count}", f"{snapshot_id}", f"{region}", "FAIL", f"{evidence}"]
                            csv_writer.writerow(row)
                        # else:
                        #     row = [f"{count}", f"{volume_id}", f"{region}", "PASS", f"{evidence}"]
                        #     csv_writer.writerow(row)
                    print(row)

                    count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
