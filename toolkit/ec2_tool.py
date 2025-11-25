import boto3
import argparse

REGION = 'ap-south-1'
ec2 = boto3.client('ec2', region_name=REGION)

def list_instances():
    response = ec2.describe_instances()
    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId': instance.get('InstanceId'),
                'State': instance.get('State', {}).get('Name'),
                'Type': instance.get('InstanceType'),
                'PublicIp': instance.get('PublicIpAddress')
            })
            
    return instances

def start_instance(instance_ids):
    response = ec2.start_instances(InstanceIds=instance_ids)
    print(f"Starting instances: {instance_ids}")
    return response

def stop_instance(instance_ids):
    response = ec2.stop_instances(InstanceIds=instance_ids)
    print(f"Stopping instances: {instance_ids}")
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS Automation Toolkit")
    parser.add_argument('action', choices=['list', 'start', 'stop'], help='Action to perform')
    parser.add_argument('instance_ids', nargs='*', help='Instance IDs (required for start/stop)')
    
    args = parser.parse_args()

    if args.action == 'list':
        print(list_instances())
        
    elif args.action in ['start', 'stop']:
        if not args.instance_ids:
            print(f"Error: The '{args.action}' action requires at least one Instance ID.")
            exit(1)

        if args.action == 'start':
            start_instance(args.instance_ids)
        elif args.action == 'stop':
            stop_instance(args.instance_ids)