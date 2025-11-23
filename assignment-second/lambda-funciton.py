import boto3
import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # ?? Replace with your bucket and optional folder/prefix
    bucket_name = 'mlal-s3'
    prefix = ''  # optional; use '' to scan entire bucket

    # Set cutoff date (90 days ago)
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=10)

    paginator = s3.get_paginator('list_objects_v2')
    deleted = 0

    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            last_modified = obj['LastModified'].replace(tzinfo=None)

            if last_modified < cutoff:
                print(f"Deleting {key} (LastModified: {last_modified})")
                s3.delete_object(Bucket=bucket_name, Key=key)
                deleted += 1

    print(f"? Deleted {deleted} files older than 90 days.")
