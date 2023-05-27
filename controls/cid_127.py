import boto3
import csv
import os

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

# AWS Account ID
AWS_ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure AWS EBS Volume snapshots are encrypted"

def main():
    print(CONTROL_DESCRIPTION)

    with open('/tmp/cid_127_controls.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Count", "Snapshot ID", "Region", "Result", "Owner ID"])
        count = 1

        for region in REGIONS:
            ec2_client = boto3.client('ec2', region)

            try:
                response = ec2_client.describe_snapshots(
                    Filters=[
                        {
                            'Name': 'encrypted',
                            'Values': ['false'],
                        },
                        {
                            'Name': 'owner-id',
                            'Values': [AWS_ACCOUNT_ID],
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
                                'Name': 'encrypted',
                                'Values': ['false'],
                            },
                            {
                                'Name': 'owner-id',
                                'Values': [AWS_ACCOUNT_ID],
                            },
                        ],
                        MaxResults=200
                    )
                    snapshots.extend(response["Snapshots"])

                for snapshot in snapshots:
                    snapshot_id = snapshot["SnapshotId"]
                    owner_id = snapshot["OwnerId"]

                    row = [f"{count}", f"{snapshot_id}", f"{region}", "FAIL", f"{owner_id}"]
                    csv_writer.writerow(row)
                    print(row)

                    count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
