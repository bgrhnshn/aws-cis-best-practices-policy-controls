import boto3
import csv
import os

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure that Unattached EBS Volumes are encrypted"

def main():
    print(CONTROL_DESCRIPTION)

    with open('cid_116_controls.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Count", "Volume ID", "Region", "Result", "Evidence"])
        count = 1

        for region in REGIONS:
            ec2_client = boto3.client('ec2', region)

            try:
                response = ec2_client.describe_volumes()
                volumes = response["Volumes"]

                for volume in volumes:
                    volume_id = volume["VolumeId"]
                    attachments = volume["Attachments"]
                    print("Processing Volume:", volume_id)

                    if len(attachments) == 0:
                        row = [f"{count}", f"{volume_id}", f"{region}", "FAIL", f"{str(attachments)}"]
                        csv_writer.writerow(row)
                        print("Row added to CSV file:", row)
                        count += 1

            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
