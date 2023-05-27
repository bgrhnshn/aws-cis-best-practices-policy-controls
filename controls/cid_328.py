import boto3
import csv

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure that EC2 instances have no public IP"

def main():
    print(CONTROL_DESCRIPTION)

    with open('/tmp/cid_328_controls.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Count", "Instance ID", "Region", "Result", "Evidence"])
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
                        instance_id = instance["InstanceId"]
                        public_ip_address = instance.get("PublicIpAddress", "")

                        if public_ip_address != "":
                            evidence = f"['PublicIpAddress': '{public_ip_address}']"
                            row = [f"{count}", f"{instance_id}", f"{region}", "FAIL", evidence]
                            csv_writer.writerow(row)
                            print(row)

                        count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
