import boto3
import csv
import os

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure that EBS Volumes attached to EC2 instances are encrypted"

# Control function
def control(ec2_client, volume_id):
    response = ec2_client.describe_volumes(
        VolumeIds=[
            volume_id
        ]
    )
    is_encrypted = response["Volumes"][0]["Encrypted"]
    evidence = response["Volumes"][0]
    if str(is_encrypted) == "False":
        return "FAIL", evidence
    elif str(is_encrypted) == "True":
        return "PASS", evidence
    else:
        return "", ""

def main():
    print(CONTROL_DESCRIPTION)

    with open('/tmp/cid_115_controls.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["#", "Volume ID", "Instance ID", "Region", "Result", "Evidence"])
        count = 1

        for region in REGIONS:
            ec2_client = boto3.client('ec2', region)

            try:
                response = ec2_client.describe_instances(
                    MaxResults=200
                )

                reservations = response["Reservations"]
                while "NextToken" in response:
                    response = ec2_client.describe_instances(
                        NextToken=response["NextToken"],
                        MaxResults=200
                    )
                    reservations.extend(response["Reservations"])

                for reservation in reservations:
                    instances = reservation["Instances"]

                    for instance in instances:
                        print("Processing Instance:", instance["InstanceId"])
                        ebs_devices = instance["BlockDeviceMappings"]

                        for device in ebs_devices:
                            volume_id = device["Ebs"]["VolumeId"]
                            result, evidence = control(ec2_client, volume_id)
                            row = [f"{count}", f"{volume_id}", f"{instance['InstanceId']}", f"{region}", f"{result}", f"{evidence}"]

                            if result == "FAIL":
                                csv_writer.writerow(row)
                                print("Row added to CSV file:", row)
                                count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
