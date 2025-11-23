## Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3
Create an AWS Lambda function using Boto3 to automatically add tags to newly launched EC2 instances. This process will be automated using an Amazon EventBridge rule, which will trigger the Lambda function upon instance creation, detect the new EC2 instance, and apply the appropriate tags.
# Objective:
Learn to automate the tagging of EC2 instances as soon as they are launched, ensuring better resource tracking and management.

# Set up IAM role for Lambda:
I created IAM role for Lambda function using following steps:
-	I went on IAM then select “Roles” screen
-	Select Trusted entity type as AWS Service and use case: Lambda
-	Attach permission policy: AmazonEC2FullAccess
-	Enter Name of the Role: EC2AutoTagLambdaRole and create the Role
-	More reference screen shots:
 <img width="940" height="424" alt="image" src="https://github.com/user-attachments/assets/f99aaf76-4476-4c9e-9bbe-66a05c426e34" />
 <img width="939" height="448" alt="image" src="https://github.com/user-attachments/assets/f446835d-6adb-40cb-96a4-7d4d8e6250ba" />
 <img width="939" height="864" alt="image" src="https://github.com/user-attachments/assets/d0df949a-2873-465b-8c59-c3b633987073" />
 <img width="938" height="266" alt="image" src="https://github.com/user-attachments/assets/7da03d98-acaf-41c8-90a4-479453e94778" />

# Create Lambda Function using Boto3:
-	I went on Lambda screen and click on “Create Function” button
-	Enter name of the function 
-	Select runtime: Python 3.12
-	Select the Execution Role under the permission section: EC2AutoTagLambdaRole (Already created IAM Role for Lambda)
-	Added the following Python code in Lambda function editor:
```
import boto3
from datetime import datetime
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    #Extract instance ID(s) from the CloudWatch event
    instances = event.get("detail", {}).get("instance-id")    if not instances:
        print("No instance ID found in the event.")
        return
    if not isinstance(instances, list):
        instances = [instances]
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    #Apply tags
    response = ec2.create_tags(
        Resources=instances,
        Tags=[
            {'Key': 'LaunchDate', 'Value': current_date},
            {'Key': 'Environment', 'Value': 'Auto-Tagged'}
        ]
    )
print(f"Successfully tagged instance(s): {instances} on {current_date}")
```
-	Deploy the above code
<img width="1920" height="2345" alt="image" src="https://github.com/user-attachments/assets/1ef086c4-74c4-469d-9b8b-01bb09f0369d" />

# Setup Amazon EventBridge Rule:
-	I went Amazon EventBridge screen then select Rule and clicked on Create button.
-	Enter name “TagNewEC2Instances-mlal”
-	Event Source: AWS events or EventBridge default bus-

-	<img width="1862" height="830" alt="image" src="https://github.com/user-attachments/assets/b5f5d5d9-1a98-4a58-aa39-ed655b8b34b0" />

# Create new EC2 Instance
- Go to Launch Instance screen
- Enter name of instance
- Select Security Key
- Assign the Key file.
- Then launch the instance and wait for 2-3 minutes then I can the tagging added to instance.
- For more reference check below screen shots:
<img width="1920" height="915" alt="Firefox_Screenshot_2025-07-03T15-07-18 544Z" src="https://github.com/user-attachments/assets/fa62ba3f-2032-449f-8709-23055410cc85" />





