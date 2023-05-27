import boto3
import csv

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ecr').describe_repositories()['repositories']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure ECR image scanning on push is enabled"

def main():
    print(CONTROL_DESCRIPTION)

    with open('/tmp/cid_377_controls.csv', mode='w', newline='') as csv_file:
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
                    repository_arn = str(repository["repositoryArn"])
                    image_scan_configuration = repository.get("imageScanningConfiguration", {})
                    evidence = f"['imageScanningConfiguration': {image_scan_configuration}]"

                    if str(image_scan_configuration.get("scanOnPush")) != "True":
                        row = [f"{count}", f"{repository_arn}", f"{region}", "FAIL", evidence]
                        csv_writer.writerow(row)
                        print(row)

                    count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
