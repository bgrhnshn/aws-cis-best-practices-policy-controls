<h1>AWS-Best-Practices-Policy-Controls</h1>

<p>This repository contains Lambda functions for implementing AWS CIS (Center for Internet Security) best practices policy controls. The functions are designed to check and enforce various security controls in an AWS environment.</p>

<h2>AWS Best Practices Policy Controls</h2>
<ul>
  <li>CID:115 - Ensure that EBS Volumes attached to EC2 instances are encrypted</li>
  <li>CID:116 - Ensure that Unattached EBS Volumes are encrypted</li>
  <li>CID:126 - Ensure AMIs owned by an AWS account are encrypted</li>
  <li>CID:127 - Ensure AWS EBS Volume snapshots are encrypted</li>
  <li>CID:203 - Ensure EBS Volume is encrypted by KMS using a customer managed Key (CMK)</li>
  <li>CID:204 - Ensure AWS EBS Volume snapshots are encrypted with KMS using a customer managed Key (CMK)</li>
  <li>CID:293 - Ensure ECR repository policy is not set to public</li>
  <li>CID:305 - Ensure ECR Image Tags are immutable</li>
  <li>CID:322 - Ensure Instance Metadata Service Version 1 is not enabled</li>
  <li>CID:328 - Ensure that EC2 instance have no public IP</li>
  <li>CID:350 - Ensure that detailed monitoring is enabled for EC2 instances</li>
  <li>CID:357 - Ensure that EC2 is EBS optimized</li>
  <li>CID:358 - Ensure that ECR repositories are encrypted using KMS</li>
  <li>CID:377 - Ensure ECR image scanning on push is enabled</li>
  <li>CID:398 - Ensure that all EIP addresses allocated to a VPC are attached to EC2 instances</li>
  <li>CID:433 - Ensure EC2 Instances are using IAM Roles</li>
  <li>CID:439 - Ensure that Elastic File System does not have the default access policy</li>
</ul>

<h2>Lambda Functions</h2>

<h3><code>Main</code> Lambda Function</h3>

<p>This Lambda function is responsible for running all the CIS best practices policy controls. It invokes individual control functions to check each control and generates control result CSV files for each control. The control results are saved in the specified S3 bucket.</p>

<h4>Configuration</h4>

<p>The <code>Main</code> Lambda function requires the following configuration:</p>
<ul>
  <li><strong>Lambda Function Role:</strong> Ensure that the Lambda function has appropriate IAM permissions to access the necessary AWS services such as EC2, EBS, ECR, etc.</li>
  <li><strong>S3 Bucket:</strong> Provide the name of the S3 bucket where the control results will be saved. The Lambda function will need write access to the bucket.</li>
</ul>

<h4>Execution</h4>

<p>The <code>Main</code> Lambda function can be scheduled to run at regular intervals using AWS CloudWatch Events or triggered manually.</p>

<h3>Control Functions</h3>

<p>The repository includes multiple control functions located in the <code>controls</code> folder. Each control function implements a specific security control and generates control result CSV files.</p>

<p>To add a new control, create a new Python file following the same structure as the existing control functions. Make sure to include the control description, necessary imports, and a <code>main()</code> function to execute the control logic.</p>

<h2>Usage</h2>

<p>To use the Lambda functions:</p>

<ol>
  <li>Clone the repository: <code>git clone https://github.com/bgrhnshn/aws-cis-best-practices-policy-controls.git</code></li>
  <li>Set up the required configurations for the <code>Main</code> Lambda function.</li>
  <li>Deploy the Lambda functions to AWS Lambda.</li>
  <li>Configure the necessary triggers or schedule the <code>Main</code> function to run at the desired intervals.</li>
  <li>Monitor the control result CSV files in the specified S3 bucket.</li>
</ol>

<h2>AWS Best Practices Policy</h2>

<p>For detailed information on AWS CIS best practices policy controls, please refer to the <a href="AWS%20Best%20Practices%20Policy.pdf">AWS Best Practices Policy document</a>.</p>

<h2>License</h2>

<p>This project is licensed under the <a href="LICENSE">MIT License</a>.</p>
