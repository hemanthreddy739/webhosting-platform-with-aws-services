import os
import boto3
from django.conf import settings
from django.shortcuts import render, redirect
from .regions_data import regions_data, ami_id_data
from django.urls import reverse
import zipfile
from botocore.exceptions import ClientError
from .launchInstance import launch_ec2_instance
from .copyProjectFromS3ToInstance import copy_project_to_ec2_instance
from .sendMail import sendmail


def zip_folder(local_folder_path):

    zip_file_path = local_folder_path + '.zip'
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(local_folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, local_folder_path)
                zipf.write(local_file_path, relative_path)
    return zip_file_path


def upload_file_to_s3(zip_file_path, region_name, projectfilename):
    
    # Construct the bucket name
    bucket_name = f"ihs-users-project-folders-bucket-{region_name}"

    # Create an S3 client
    s3 = boto3.client('s3', region_name=region_name)

    # Check if the bucket exists
    try:
        s3.head_bucket(Bucket=bucket_name)
    except s3.exceptions.ClientError as e:
        # Bucket does not exist, create it
        if e.response['Error']['Code'] == '404':
            create_bucket_config = {
                'LocationConstraint': region_name,
            }

            try:
                s3.create_bucket(Bucket=bucket_name, 
                                 CreateBucketConfiguration=create_bucket_config
                                 )
                print(f"Created bucket '{bucket_name}' in region '{region_name}'")
            except Exception as e:
                print(f"Error creating bucket '{bucket_name}': {e}")
            

    # Check if the file exists in the bucket
    try:
        s3.head_object(Bucket=bucket_name, Key= projectfilename)
        print(f"File '{projectfilename}' already exists in bucket '{bucket_name}'")
    except s3.exceptions.ClientError as e:
        # File does not exist, upload it
        if e.response['Error']['Code'] == '404':
            try:
                s3.upload_file(zip_file_path, bucket_name, projectfilename)
                print(f"Uploaded file '{projectfilename}' to bucket '{bucket_name}'")
            except Exception as e:
                print(f"Error uploading file '{projectfilename}' to bucket '{bucket_name}': {e}")



def hostproject(request):
    code = request.GET.get('code')
   
    if request.method == 'POST':

        # collecting data from the 'hosting_input_data_form'
        project_name = request.POST.get('projectName')
        absolute_path = request.POST.get('absolutePath')
        chosen_region = request.POST.get('chosenRegion')
        
        # Replace backslashes with forward slashes
        project_path = os.path.abspath(absolute_path).replace('\\', '/')

        projectfilename = project_name + '.zip'  # Use project name as the S3 key with .zip extension
            
        # getting the properties to launch an instance with that properties
        aws_region_name = regions_data[chosen_region]
        ami_id = ami_id_data[aws_region_name]

        
        zip_file_path = zip_folder(project_path)
        upload_file_to_s3(zip_file_path, aws_region_name, projectfilename)


        # now launching instance
        launched_instance_id = launch_ec2_instance(aws_region_name, ami_id)

        # now copying the project from the bucket to the launhedInstance
        webpage_url, instance_ip = copy_project_to_ec2_instance(
            aws_region_name, launched_instance_id, projectfilename
        )

        if webpage_url:
            sendmail(code, instance_ip)

            # after successfullly hosting the webpage, rendering success page
            return redirect(reverse('hostingsuccess') + f'?webpage_url={webpage_url}')
        else:
            return redirect('hostingfailed')
    
    else:
        city_names = list(regions_data.keys())
        context = {'city_names': city_names, 'pageTitle':"Host Project"}
        return render(request, 'grabproject/host_project.html', context)



def instancebuilding(request):
    
    context = {'pageTitle':"ServerBuilding"}
    return render(request, 'grabproject/instanceBuilding.html', context)


def hostingsuccess(request):
    webpage_url = request.GET.get('webpage_url')
    context = {'webpage_url': webpage_url}
    return render(request, 'grabproject/hostingsuccess.html', context)


def hostingfailed(request):
    return render(request, 'grabproject/hostingfailed.html')


def ihsLogin(request):
    return redirect('https://ihs.auth.ap-south-1.amazoncognito.com/login?client_id=49n2v2j0bjrbvb9464tlg4spit&response_type=code&scope=email+openid+phone&redirect_uri=http://localhost:8000/hostproject')


def loggedout(request):
    return render(request, 'loggedout.html')





