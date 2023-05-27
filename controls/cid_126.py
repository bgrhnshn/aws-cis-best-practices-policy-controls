import boto3
import csv
import os

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure AMIs owned by an AWS account are encrypted"

def main():
    print(CONTROL_DESCRIPTION)

    with open('cid_126_controls.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Count", "Image ID", "Region", "Result", "Owner ID", "Evidence"])
        count = 1

        for region in REGIONS:
            ec2_client = boto3.client('ec2', region)

            try:
                response = ec2_client.describe_images(
                    Filters=[
                        {
                            'Name': 'is-public',
                            'Values': ['false'],
                        },
                        {
                            'Name': 'block-device-mapping.encrypted',
                            'Values': ['false'],
                        },
                        {
                            'Name': 'image-type',
                            'Values': ['machine'],
                        },
                    ]
                )

                images = response["Images"]

                for image in images:
                    image_id = image["ImageId"]
                    owner_id = image["OwnerId"]
                    evidence = str(image["BlockDeviceMappings"])

                    row = [f"{count}", f"{image_id}", f"{region}", "FAIL", f"{owner_id}", f"{evidence}"]
                    csv_writer.writerow(row)
                    print(row)

                    count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
