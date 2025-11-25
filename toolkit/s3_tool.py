import boto3
import argparse
import os
from botocore.exceptions import ClientError

def list_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    
    
    buckets = []
    for bucket in response['Buckets']:
        buckets.append(bucket['Name'])
        
    return buckets

def create_bucket(bucket_name, region_name=None):
    region = region_name
    s3 = boto3.client('s3', region_name=region)

    if region == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )

def upload_file(bucket_name, file_name, object_name=None):
    s3 = boto3.client('s3')
    
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"Uploaded {file_name} to {bucket_name}/{object_name}")
    except ClientError as e:
        print(f"File upload failed: {e}")
        return False
    return True

def list_objects(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        
        print(f"Files in '{bucket_name}'")
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"{obj['Key']} (Size: {obj['Size']} bytes)")
        else:
            print(" (Bucket is empty)")
            
    except ClientError as e:
        print(f"Error listing objects in '{bucket_name}': {e}")

def delete_bucket(bucket_name, empty_first=False):
    s3 = boto3.client('s3')

    if empty_first:
        try:
            print(f"Emptying bucket '{bucket_name}'...")
            response = s3.list_objects_v2(Bucket=bucket_name)
            
            if 'Contents' in response:
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
                s3.delete_objects(
                    Bucket=bucket_name, 
                    Delete={'Objects': objects_to_delete}
                )
                print(f" - Deleted {len(objects_to_delete)} objects.")
            else:
                print(" - Bucket was already empty.")
                
        except ClientError as e:
            print(f"Error checking/emptying bucket: {e}")
            return

    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' deleted successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketNotEmpty':
            print(f"Error: Bucket '{bucket_name}' is not empty. Use the --empty flag to delete contents first.")
        else:
            print(f"Could not delete bucket '{bucket_name}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS Automation Toolkit")
    parser.add_argument('action', choices=['list', 'create', 'upload', 'delete'], help="Action to perform.")
    parser.add_argument('buckets', nargs='*', help="Choose a unique name for the bucket.")
    parser.add_argument('--region_name', default='ap-south-1', help="Choose a region for the bucket (ap-south-1 by default).")
    parser.add_argument('--file_name', help="File name to upload to the bucket.")
    parser.add_argument('--object_name', help="S3 object name. If not specified then file_name is used.")
    parser.add_argument('--empty', action='store_true', help="Delete all files in the bucket before deleting the bucket itself.")
    

    args = parser.parse_args()

    if args.action == 'list':
        if args.buckets:
            for bucket in args.buckets:
                list_objects(bucket)
        else:
            print("Existing Buckets:")
            print(list_buckets())
    
    elif(args.action == 'create'):
        if not args.buckets:
            print("Error: Enter atleast one bucket name.")
            exit(1)
        for bucket in args.buckets:
            try:
                print(f"Creating the bucket: {bucket}")
                create_bucket(bucket, args.region_name)
                print("Bucket created successfully.")
            except ClientError as e:
                print(f"Bucket creation failed for '{bucket}': {e}")

    elif args.action == 'upload':
        if not args.buckets or not args.file_name:
            print("Error: Enter atleast one bucket name and file name.")
            exit(1)
        for bucket in args.buckets:
            upload_file(bucket, args.file_name, args.object_name)

    elif args.action == 'delete':
        if not args.buckets:
            print("Error: 'delete' requires at least one bucket name.")
            exit(1)
        for bucket in args.buckets:
            delete_bucket(bucket, empty_first=args.empty)