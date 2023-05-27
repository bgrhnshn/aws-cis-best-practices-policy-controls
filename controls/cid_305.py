import boto3
import csv

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure ECR Image Tags are immutable"

def main():
    print(CONTROL_DESCRIPTION)

    with open('/tmp/cid_305_controls.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Count", "Repository ARN", "Region", "Result", "Evidence"])
        count = 1

        for region in REGIONS:
            ecr_client = boto3.client('ecr', region)

            try:
                response = ecr_client.describe_repositories(
                    maxResults=200
                )

                repositories = response["repositories"]

                while "NextToken" in response:
                    response = ecr_client.describe_repositories(
                        nextToken=response["NextToken"],
                        maxResults=200
                    )
                    repositories.extend(response["repositories"])

                for repository in repositories:
                    repository_arn = repository["repositoryArn"]
                    image_mutability = str(repository["imageTagMutability"])
                    evidence = f"['imageTagMutability': '{image_mutability}']"
                    if image_mutability != "IMMUTABLE":
                        row = [f"{count}", f"{repository_arn}", f"{region}", "FAIL", f"{evidence}"]
                        csv_writer.writerow(row)
                        print(row)

                    count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
