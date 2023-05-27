import boto3
import csv

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_addresses()['Addresses']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure that all EIP addresses allocated to a VPC are attached to EC2 instances"

def main():
    print(CONTROL_DESCRIPTION)

    with open('/tmp/cid_398_controls.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Count", "Public IP", "Region", "Result", "Evidence"])
        count = 1

        for region in REGIONS:
            ec2_client = boto3.client('ec2', region)

            try:
                response = ec2_client.describe_addresses()

                addresses = response["Addresses"]

                for address in addresses:
                    public_ip = address["PublicIp"]
                    associated_instance = address.get("InstanceId")

                    evidence = f"['InstanceId': '{associated_instance}']"

                    if not associated_instance:
                        row = [f"{count}", f"{public_ip}", f"{region}", "FAIL", evidence]
                        csv_writer.writerow(row)
                        print(row)

                    count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
