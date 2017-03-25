import boto3
import pprint

"""
Create .env file 

$ vim .env 
------------------ 
access_key=xxxxxx
secret_key=xxxxxx
region=us-west-2
~
~
~
".env" [New File]
"""

with open('.env', 'r') as f:
    content = f.readlines()

env = dict([line.strip().split("=") for line in content if '=' in line])

# Credentials & Region
access_key = env.get('access_key')
secret_key = env.get('secret_key')
region = env.get('region')

# ECS Details
cluster_name = "BotoCluster"
service_name = "service_hello_world"
task_name = "hello_world"

# Let's use Amazon ECS
ecs_client = boto3.client(
    'ecs',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

# Let's use Amazon EC2
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

def launch_ecs_example():
    response = ecs_client.create_cluster(
        clusterName=cluster_name
    )

    pprint.pprint(response)

    # Create EC2 instance(s) in the cluster
    # For now I expect a default cluster to be there

    # By default, your container instance launches into your default cluster.
    # If you want to launch into your own cluster instead of the default,
    # choose the Advanced Details list and paste the following script
    # into the User data field, replacing your_cluster_name with the name of your cluster.
    # !/bin/bash
    # echo ECS_CLUSTER=your_cluster_name >> /etc/ecs/ecs.config

    response = ec2_client.run_instances(
        # Use the official ECS image
        ImageId="ami-5e63d13e",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        IamInstanceProfile={
            "Name": "ecsInstanceRole"
        },
        UserData="#!/bin/bash \n echo ECS_CLUSTER=" + cluster_name + " >> /etc/ecs/ecs.config"
    )

    pprint.pprint(response)

    # Create a task definition
    response = ecs_client.register_task_definition(
        containerDefinitions=[
        {
          "name": "wordpress",
          "links": [
            "mysql"
          ],
          "image": "wordpress",
          "essential": True,
          "portMappings": [
            {
              "containerPort": 80,
              "hostPort": 80
            }
          ],
          "memory": 300,
          "cpu": 10
        },
        {
          "environment": [
            {
              "name": "MYSQL_ROOT_PASSWORD",
              "value": "password"
            }
          ],
          "name": "mysql",
          "image": "mysql",
          "cpu": 10,
          "memory": 300,
          "essential": True
        }
        ],
        family="hello_world"
    )

    pprint.pprint(response)

    # Create service with exactly 1 desired instance of the task
    # Info: Amazon ECS allows you to run and maintain a specified number
    # (the "desired count") of instances of a task definition
    # simultaneously in an ECS cluster.

    response = ecs_client.create_service(
        cluster=cluster_name,
        serviceName=service_name,
        taskDefinition=task_name,
        desiredCount=1,
        clientToken='request_identifier_string',
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 50
        }
    )

    pprint.pprint(response)


# Shut everything down and delete task/service/instance/cluster
def terminate_ecs_example():
    try:
        # Set desired service count to 0 (obligatory to delete)
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service_name,
            desiredCount=0
        )
        # Delete service
        response = ecs_client.delete_service(
            cluster=cluster_name,
            service=service_name
        )
        pprint.pprint(response)
    except:
        print("Service not found/not active")

    # List all task definitions and revisions
    response = ecs_client.list_task_definitions(
        familyPrefix=task_name,
        status='ACTIVE'
    )

    # De-Register all task definitions
    for task_definition in response["taskDefinitionArns"]:
        # De-register task definition(s)
        deregister_response = ecs_client.deregister_task_definition(
            taskDefinition=task_definition
        )
        pprint.pprint(deregister_response)

    # Terminate virtual machine(s)
    response = ecs_client.list_container_instances(
        cluster=cluster_name
    )
    if response["containerInstanceArns"]:
        container_instance_resp = ecs_client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=response["containerInstanceArns"]
        )
        for ec2_instance in container_instance_resp["containerInstances"]:
            ec2_termination_resp = ec2_client.terminate_instances(
                DryRun=False,
                InstanceIds=[
                    ec2_instance["ec2InstanceId"],
                ]
            )

    # Finally delete the cluster
    response = ecs_client.delete_cluster(
        cluster=cluster_name
    )
    pprint.pprint(response)


launch_ecs_example()
terminate_ecs_example()