import boto3
import time

# AWS credentials and region
aws_access_key_id = ''
aws_secret_access_key = ''
region = 'us-east-1'

# Initialize EC2 client
ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key,
                   region_name=region)

# Create EC2 instance
def create_ec2_instance():
    response = ec2.run_instances(
        ImageId='ami-0fa1ca9559f1892ec',  # Replace with your AMI ID
        InstanceType='t2.micro',  # Replace with desired instance type
        MinCount=1,
        MaxCount=1,
        KeyName='cmbkey',  # Replace with your key pair name
        SecurityGroups=['WebServerSecurityGroup']  # Replace with your security group
    )
    return response['Instances'][0]['InstanceId']

# Get public IP of the instance
def get_instance_public_ip(instance_id):
    instance = ec2.describe_instances(InstanceIds=[instance_id])
    return instance['Reservations'][0]['Instances'][0]['PublicIpAddress']

if __name__ == "__main__":
    # Create EC2 instance
    instance_id = create_ec2_instance()
    print(f"EC2 Instance {instance_id} is being created...")

    # Wait for the instance to be running
    instance_state = ''
    while instance_state != 'running':
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        instance_state = instance['Reservations'][0]['Instances'][0]['State']['Name']
        time.sleep(5)

    # Once the instance is running, fetch and display the public IP
    public_ip = get_instance_public_ip(instance_id)
    print(f"EC2 Instance Public IP: {public_ip}")
