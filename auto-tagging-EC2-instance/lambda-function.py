import boto3
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Extract instance ID from the CloudWatch event
    instance_id = event['detail']['instance-id']

    # Generate current date string
    launch_date = datetime.utcnow().strftime('%Y-%m-%d')

    # Define tags to apply
    tags = [
        {'Key': 'LaunchDate', 'Value': launch_date},
        {'Key': 'Environment', 'Value': 'Development'}  # you can customize this
    ]

    # Apply tags to the instance
    ec2.create_tags(
        Resources=[instance_id],
        Tags=tags
    )

    print(f"Tagged instance {instance_id} with {tags}")
    return {
        'statusCode': 200,
        'body': f"Instance {instance_id} tagged successfully"
    }

