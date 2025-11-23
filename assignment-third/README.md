## Auto-Autosave EC2 Instance State Before Shutdown
Create an AWS Lambda function using Boto3 to be an EC2 instance is shut down, automatically save its current state to an S3 bucket. This process will be automated using an Amazon EventBridge rule, which will trigger the Lambda function upon instance during the termination of instance.
Objective:
Automatically back up metadata of an EC2 instance to an S3 bucket before termination, to assist with auditing, diagnostics, or record-keeping.

# Set up IAM role for Lambda:
I created IAM role for Lambda function using following steps:
-	I went on IAM then select “Roles” screen
-	Select Trusted entity type as AWS Service and use case: Lambda
-	Attach permission policy: AmazonEC2FullAccess and AmazonEC2ReadOnlyAccess
-	Enter Name of the Role: EC2ShutdownBackupsLambdaRole-Mlal and create the Role
-	More reference screen shots:
<img width="940" height="424" alt="image" src="https://github.com/user-attachments/assets/184213a3-f3b3-46f5-b42c-ec840f9f0995" />
<img width="940" height="461" alt="image" src="https://github.com/user-attachments/assets/f4fe9720-a9bf-40a8-9340-1badfd4311de" />

# Create Lambda Function using Boto3:
-	I went on Lambda screen and click on “Create Function” button
-	Enter name of the function 
-	Select runtime: Python 3.12
-	Select the Execution Role under the permission section: EC2TerminateBackup-Mlal (Already created IAM Role for Lambda)
-	Added the following Python code in Lambda function editor:
  ```
import boto3
from datetime import datetime
import boto3
import json
from datetime import datetime
def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    s3_client = boto3.client('s3')
    #Extract instance ID from the event
    instance_id = event['detail'].get('instance-id')
    if not instance_id:
        print("No instance ID found in event.")
        return
    #Fetch instance description
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance_info = response['Reservations'][0]['Instances'][0]
    #Prepare data to save
    backup_data = {
        'InstanceId': instance_id,
        'State': instance_info.get('State', {}).get('Name'),
        'LaunchTime': str(instance_info.get('LaunchTime')),
        'InstanceType': instance_info.get('InstanceType'),
        'Tags': instance_info.get('Tags', [])
    }
    #Save to S3
    bucket_name = 'ec2-state-backups-mlal'
    key = f"backups/{instance_id}-{datetime.utcnow().isoformat()}.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(backup_data),
        ContentType='application/json'
    )
    print(f"? Backup of {instance_id} saved to {bucket_name}/{key}")
```
-	Deploy the above code
<img width="940" height="620" alt="image" src="https://github.com/user-attachments/assets/e063d0ed-9922-431e-8d79-79c5fd0ed724" />

# Setup Amazon EventBridge Rule:
  -	I went Amazon EventBridge screen then select Rule and clicked on Create button.
  -	Enter name “EC2ShutdownTrigger-mlal”
  -	Event Source: AWS events or EventBridge default bus
 <img width="940" height="408" alt="image" src="https://github.com/user-attachments/assets/722c8050-4e7e-480d-9eb5-a0ccbea70298" />

# Create A S3 bucket:
  -	I used following path to create bucket:	S3-> Create Bucket-> Bucket Name
  -	I gave bucket name: ec2-state-backups-mlal
 <img width="940" height="278" alt="image" src="https://github.com/user-attachments/assets/02d2a7ea-a585-4739-8b6d-1b649a7bf170" />

# Testing Steps:
  -	Launch an EC2 instance
  -	Terminate it via EC2 dashboard or CLI
  -	Within ~1 minute:
      o	Check the S3 bucket for the .json backup
      o	Check CloudWatch Logs for confirmation

