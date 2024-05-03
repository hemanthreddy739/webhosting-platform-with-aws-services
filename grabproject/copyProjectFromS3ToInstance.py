import boto3
import time
from fabric import Connection




# waitig for the instance to come into the running state
def wait_until_instance_running(instance_id, region_name):
    ec2 = boto3.resource('ec2', region_name=region_name)
    instance = ec2.Instance(instance_id)
    print("Waiting for the instance to be running...")
    instance.wait_until_running()
    print("Instance is now running.")


# downloading the projectfolder from the 's3' bucket into the 'ec2'

def copy_project_to_ec2_instance(region_name, instance_id, projectfilename):
    # Wait for the instance to be running
    wait_until_instance_running(instance_id, region_name)

    time.sleep(120)

    # Connect to the EC2 instance via SSH
    instance = boto3.resource('ec2', region_name=region_name).Instance(instance_id)
    instance_ip = instance.public_ip_address

    print(f"Connecting to EC2 instance {instance_id} ({instance_ip})...")

    # Replace 'your-password' with the actual password
    password = 'password-of-user(created during launch time of ec2)'


    bucket_name = f"ihs-users-project-folders-bucket-{region_name}"

    webpage_url = ''
    
    

    try:
        # Connect to the instance using Fabric
        with Connection(host=instance_ip, user='user-name(created during launch time of ec2)', connect_kwargs={'password': password}) as c:
            # Execute command to retrieve folder from S3 and move it to /var/www/html
            c.run(f"sudo aws s3 cp s3://{bucket_name}/{projectfilename} /var/www/html")
            c.run(f"sudo unzip /var/www/html/{projectfilename} -d /var/www/html")

            print(f"Folder '{projectfilename}' copied to /var/www/html on EC2 instance {instance_id}.")
            print("click on the below link to see your webpage")
            print(f"http://{instance_ip}")

            webpage_url += f'http://{instance_ip}'

    except Exception as e:
        print(f"An error occurred: {e}")

    return (webpage_url, instance_ip)
