import boto3
import csv

# AWS Regions
REGIONS = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

# Explanation of Control
CONTROL_DESCRIPTION = "Ensure ECR repository policy is not set to public"

def main():
    print(CONTROL_DESCRIPTION)

    with open('/tmp/cid_293_controls.csv', mode='w', newline='') as csv_file:
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
                    repository_name = str(repository["repositoryName"])
                    repository_arn = str(repository["repositoryArn"])

                    try:
                        response = ecr_client.get_repository_policy(
                            repositoryName=repository_name
                        )
                        row = [f"{count}", f"{repository_arn}", f"{region}", "FAIL", f"{response}"]
                        csv_writer.writerow(row)
                        print(row)
                    except:
                        pass

                    count += 1
            except Exception as e:
                print(f"Exception in region {region}: {str(e)}")
