## Auto-Implement a Log Cleaner for S3
Create an AWS Lambda function using Boto3 to cleanup the S3 bucket by scheduled time automatically. This process will be automated using an Amazon EventBridge rule, which will trigger the Lambda function upon s3 bucket location.
# Objective:
Create a Lambda function that automatically deletes logs in a specified S3 bucket that are older than 90 days.
# Set up IAM role for Lambda:
I created IAM role for Lambda function using following steps:
  -	I went on IAM then select “Roles” screen
  -	Select Trusted entity type as AWS Service and use case: Lambda
  -	Attach permission policy: AmazonS3FullAccess 
  -	Enter Name of the Role: LambdaS3CleanupRole-mlal and create the Role
  -	More reference screen shots:
 <img width="940" height="424" alt="image" src="https://github.com/user-attachments/assets/9e82b580-b910-4d0f-8b92-bda2bc815551" />
 <img width="940" height="384" alt="image" src="https://github.com/user-attachments/assets/9ddbaca0-e6fd-47b2-955f-9e8288ee2f44" /> 

# Create Lambda Function using Boto3:
-	I went on Lambda screen and click on “Create Function” button
-	Enter name of the function 
-	Select runtime: Python 3.12
-	Select the Execution Role under the permission section:   DeleteOldS3Log
-	 (Already created IAM Role for Lambda)
-	Added the following Python code in Lambda function editor:
  ```
-	import boto3
-	import datetime
-	
-	def lambda_handler(event, context):
-	    s3 = boto3.client('s3')
-	
-	    #Replace with your bucket and optional folder/prefix
-	    bucket_name = 'mlal-s3'
-	    prefix = ''  # optional; use '' to scan entire bucket
-	
-	    #Set cutoff date (90 days ago)
-	    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=10)
-	
-	    paginator = s3.get_paginator('list_objects_v2')
-	    deleted = 0
-	
-	    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
-	        for obj in page.get('Contents', []):
-	            key = obj['Key']
-	            last_modified = obj['LastModified'].replace(tzinfo=None)
-	
-	            if last_modified < cutoff:
-	                print(f"Deleting {key} (LastModified: {last_modified})")
-	                s3.delete_object(Bucket=bucket_name, Key=key)
-	                deleted += 1
-	
-	    print(f"✅ Deleted {deleted} files older than 90 days.")
```
-	Deploy the above code
 <img width="940" height="353" alt="image" src="https://github.com/user-attachments/assets/a491ded8-9936-4656-b0d7-73d066db9812" />


# Setup Amazon EventBridge Rule:
  -	I went Amazon EventBridge screen then select Rule and clicked on Create button.
  -	Enter name “S3-bucket-cleanup-mlal”
  -	Type: Schedule
 <img width="940" height="430" alt="image" src="https://github.com/user-attachments/assets/929eb8db-24e4-4988-a26e-bffc7d92d5bb" />
 
# Create A S3 bucket:
  -	I used following path to create bucket:	S3-> Create Bucket-> Bucket Name
  -	I gave bucket name: mlal-s3
 <img width="940" height="301" alt="image" src="https://github.com/user-attachments/assets/14911aa9-aa3f-41ce-9ccf-1e604f344d8b" />


# Testing Steps:
-	Upload test files (with older time)
-	Run the Lambda function manually via the Test button
-	Check:
    o	S3 bucket (old files should be gone)
    o	CloudWatch Logs for output and deletion info
