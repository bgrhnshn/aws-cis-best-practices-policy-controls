import boto3
import csv

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_addresses()['Addresses']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure that Elastic File System does not have the default access policy"

def main():
    print(CONTROL_DESCRIPTION)

    with open('/tmp/cid_439_controls.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Count", "File System Arn", "Region", "Result", "Evidence"])
        count = 1

        for region in REGIONS:
            efs_client = boto3.client('efs', region)

            try:
                response = efs_client.describe_file_systems()

                file_systems = response["FileSystems"]

                for file_system in file_systems:
                    file_system_id = file_system["FileSystemId"]
                    file_system_arn = file_system["FileSystemArn"]

                    try:
                        response = efs_client.describe_file_system_policy(FileSystemId=file_system_id)

                        # Policy exists, so it's not the default policy
                        continue
                    except efs_client.exceptions.PolicyNotFound:
                        evidence = f"['FileSystemId': '{file_system_id}', 'Policy': '']"

                        row = [f"{count}", f"{file_system_arn}", f"{region}", "FAIL", evidence]
                        csv_writer.writerow(row)
                        print(row)
                        count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
