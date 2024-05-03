import boto3
import time
from .requirementsToLaunchInstance import getUserDataScript, get_or_create_security_group, getInstanceType

# launching an instance
def launch_ec2_instance(region_name, ami_id):
    # get instance-type 
    instance_type  = getInstanceType(region_name)
    # first creating the security group in that region 'defult' vpc
    security_group_id = get_or_create_security_group(region_name)
    # Specify the IAM role for the instance
    iam_instance_profile = { 'Name': "Ec2BondWithS3" }
    # userdata_script
    userdata_script = getUserDataScript()
    # now launhing the ec2
    ec2 = boto3.client('ec2', region_name=region_name)
    response = ec2.run_instances(
        ImageId= ami_id,
        InstanceType= instance_type,
        SecurityGroupIds= [security_group_id],
        IamInstanceProfile= iam_instance_profile,
        UserData= userdata_script,
        MinCount= 1,
        MaxCount= 1
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"EC2 instance {instance_id} is launching...")

    return instance_id
