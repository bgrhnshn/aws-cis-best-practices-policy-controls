import boto3
import os
import datetime
import importlib.util

# Define your S3 bucket name here
S3_BUCKET_NAME = 'tst123214512674812416247128941'
RESULTS_FOLDER = 'control_results'

def upload_results_to_s3(account_id, date):
    """Upload all control results to S3"""
    s3_client = boto3.client('s3')
    control_files = [f for f in os.listdir('/tmp') if f.endswith('_controls.csv')]
    for control_file in control_files:
        # Create S3 object name based on account_id and date
        object_name = f"{RESULTS_FOLDER}/{account_id}/{date}/{control_file}"
        try:
            s3_client.upload_file(f'/tmp/{control_file}', S3_BUCKET_NAME, object_name)
            print(f"Uploaded {control_file} to s3://{S3_BUCKET_NAME}/{object_name}")
        except Exception as e:
            print(f"Error uploading {control_file} to S3: {str(e)}")

def run_controls():
    """Import and run all control functions from controls folder"""
    # Define the path to the controls folder
    controls_folder = './controls'
    # Get a list of all control scripts in the controls folder
    control_scripts = [f for f in os.listdir(controls_folder) if f.endswith('.py')]

    # Dynamically import and run all controls
    for control_script in control_scripts:
        # Import the control module
        spec = importlib.util.spec_from_file_location("module.name", f"{controls_folder}/{control_script}")
        control_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(control_module)
        # Run the control
        print("-------------------------------------------------")
        print(f"[+] Running control: {control_script}\n")
        control_module.main()
        print(f"\n[+] Finished running control: {control_script}")

    # After all controls have been run and results saved to CSV files,
    # upload the CSV files to S3
    print("Uploading results to S3...")
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    upload_results_to_s3(account_id, date)
    print("Finished uploading results to S3.")

def lambda_handler(event, context):
    """AWS Lambda function entrypoint"""
    run_controls()