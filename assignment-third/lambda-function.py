import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    s3_client = boto3.client('s3')

    # Extract instance ID from the event
    instance_id = event['detail'].get('instance-id')
    if not instance_id:
        print("No instance ID found in event.")
        return

    # Fetch instance description
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance_info = response['Reservations'][0]['Instances'][0]

    # Prepare data to save
    backup_data = {
        'InstanceId': instance_id,
        'State': instance_info.get('State', {}).get('Name'),
        'LaunchTime': str(instance_info.get('LaunchTime')),
        'InstanceType': instance_info.get('InstanceType'),
        'Tags': instance_info.get('Tags', [])
    }

    # Save to S3
    bucket_name = 'ec2-state-backups-mlal'
    key = f"backups/{instance_id}-{datetime.utcnow().isoformat()}.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(backup_data),
        ContentType='application/json'
    )

    print(f"? Backup of {instance_id} saved to {bucket_name}/{key}")
