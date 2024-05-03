import boto3
import time

# Read user data script content
def getUserDataScript():
    with open("C:/Users/I7013/OneDrive - Indium Software India Private Limited/Desktop/STATIC_WEB_HOSTING/static_webpage_hosting/grabproject/userdata.sh", "r") as f:
        user_data = f.read()

    return user_data


# creating an security groups
def get_or_create_security_group(region_name):
    # Create EC2 client
    ec2 = boto3.client('ec2', region_name=region_name)

    # Get default VPC ID for the region
    response = ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
    vpc_id = response['Vpcs'][0]['VpcId']

    # Define security group name
    security_group_name = 'IHS_Webserver_SG'

    # Check if the security group already exists
    try:
        response = ec2.describe_security_groups(
            Filters=[
                {'Name': 'group-name', 'Values': [security_group_name]},
                {'Name': 'vpc-id', 'Values': [vpc_id]}
            ]
        )
        existing_security_group = response['SecurityGroups'][0]
        security_group_id = existing_security_group['GroupId']
        print(f"Security group '{security_group_name}' already exists in {region_name} region.")
    except IndexError:
        # If the security group doesn't exist, create a new one
        response = ec2.create_security_group(
            GroupName=security_group_name,
            Description='Security group for IHS Web Server',
            VpcId=vpc_id
        )
        time.sleep(5)  # Wait for the security group to be created
        security_group_id = response['GroupId']
        print(f"Security group '{security_group_name}' created successfully in {region_name} region.")

        # Define inbound rules for SSH, HTTP, and HTTPS
        inbound_permissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 443,
                'ToPort': 443,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]

        # Authorize inbound rules
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=inbound_permissions
        )

        print("Inbound rules for SSH, HTTP, and HTTPS added to the security group.")

    return security_group_id




def getInstanceType(region_name):
    ec2_client = boto3.client('ec2', region_name=region_name)
    
    try:
        response = ec2_client.describe_instance_type_offerings()
        instance_types = [offering['InstanceType'] for offering in response['InstanceTypeOfferings']]
        
        if 't2.micro' in instance_types:
            return 't2.micro'
        else:
            return 't3.micro'
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    