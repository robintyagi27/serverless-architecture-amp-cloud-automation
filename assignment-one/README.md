## Automated Instance Management Using AWS Lambda and Boto3
Lambda function has been created which is managing the EC2 instances automatically.
# Objective
In this assignment, you will gain hands-on experience with AWS Lambda and Boto3, Amazon's SDK for Python. You will create a Lambda function that will automatically manage EC2 instances based on their tags.

# Setup EC2 Instances:
Log in to AWS Management Console. Navigate to EC2 Dashboard and click "Launch Instance". Choose Ubuntu Server as the OS, instance type and key pair for SSH access. Configure Security Group to allow ports and launches two EC2 instances using below details:
Instance 1: Tag as
	Key: Action and Value: Auto-Stop
Instance 2: Tag as
	Key: Action and Value: Auto-Start
 <img width="940" height="51" alt="image" src="https://github.com/user-attachments/assets/abd60c22-0a0c-49d4-9825-5ed2835bb5ea" />

# Set up IAM role for Lambda:
I created IAM role for Lambda function using following steps:
-	I went on IAM then select “Roles” screen
-	Select Trusted entity type as AWS Service and use case: Lambda
-	Attach permission policy: AmazonEC2FullAccess
-	Enter Name of the Role: LambdaEC2ControllerRole and create the Role
-	More reference screen shots:
 
 <img width="940" height="424" alt="image" src="https://github.com/user-attachments/assets/a1aac6ab-3755-4a20-9444-6ec5574e134f" />
<img width="939" height="349" alt="image" src="https://github.com/user-attachments/assets/20ea7f22-8860-454b-a548-b6ab22af7550" />
<img width="939" height="311" alt="image" src="https://github.com/user-attachments/assets/824f848a-dc01-416c-90dc-2dde0b614536" />
<img width="939" height="533" alt="image" src="https://github.com/user-attachments/assets/1319bfa4-f395-4a48-b11e-f9ac256dcf8a" />

# Create Lambda Function to manage the instances using Boto3:
-	I went on Lambda screen and click on “Create Function” button
-	Enter name of the function 
-	Select runtime: Python 3.12
-	Select the Execution Role under the permission section: LambdaEC2ControllerRole (Already created IAM Role for Lambda)
-	Added the following Python code in Lambda function editor:
```
import boto3
def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    #Filter and stop instances tagged with Auto-Stop
   stop_instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}]
    )
    stop_ids = [instance.id for instance in stop_instances if instance.state['Name'] != 'stopped']
    if stop_ids:
        ec2.instances.filter(InstanceIds=stop_ids).stop()
        print(f"Stopped instances: {stop_ids}")
    else:
        print("No instances to stop.")
    # Filter and start instances tagged with Auto-Start
    start_instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}]
    )
    start_ids = [instance.id for instance in start_instances if instance.state['Name'] != 'running']
    if start_ids:
        ec2.instances.filter(InstanceIds=start_ids).start()
        print(f"Started instances: {start_ids}")
    else:
        print("No instances to start.")
```
-	Deploy the above code
-	Description for Python Code:
    o	Initialized a boto3 EC2 client.
    o	Described instances with Auto-Stop and Auto-Start tags.
    o	Stop the Auto-Stop instances and start the Auto-Start instances.
    o	Print instance IDs that were affected for logging purposes.
-	For reference use below screen shots:
 <img width="940" height="680" alt="image" src="https://github.com/user-attachments/assets/f6359b60-3c52-4416-be4b-b4a439db503c" />
 <img width="939" height="1181" alt="image" src="https://github.com/user-attachments/assets/064ce1dc-7899-4148-a32f-770b2a05c295" />


 
# Run/Test the function:
-	Click on “Test” button then select “Create new test event”
-	Entered the Event Name
-	I did not change template and Event Sharing String leave those as it is. 
-	After that I click on “Invoke” Button
-	I went on EC2 Dashboard and checked following things:
    o	Auto-Stop instance is going to stopping
    o	Auto-Start instance is going to starting( Actually I stopped this instance for testing purpose)
-	For more reference see the below screen shots:
-	<img width="939" height="828" alt="image" src="https://github.com/user-attachments/assets/0c8f458c-2816-49e3-bb5c-924d2a450c35" />
<img width="939" height="1181" alt="image" src="https://github.com/user-attachments/assets/7f98495c-e478-4065-aa7d-b5f8533ffe1e" />
<img width="939" height="909" alt="image" src="https://github.com/user-attachments/assets/0cd74145-7840-483e-a8b5-a11b14d9f952" />
<img width="939" height="1278" alt="image" src="https://github.com/user-attachments/assets/730b31d9-d230-4eb3-a229-0368051babba" />
<img width="939" height="838" alt="image" src="https://github.com/user-attachments/assets/20e09b44-78df-4d81-b9c7-ef1b4e5bcc28" />
<img width="939" height="448" alt="image" src="https://github.com/user-attachments/assets/cab241c5-b362-4401-a3a4-8124a1979662" />






 
 
 
 
  




