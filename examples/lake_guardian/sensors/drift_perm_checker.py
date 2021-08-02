import boto3
import json


cf = boto3.client("cloudformation")
lf = boto3.client("lakeformation")


LAKE_FORMATION_RESOURCE_TYPE = {
    "table": "Table"
}


def __resource_type(resource_arn: str):
    # arn: aws: glue: eu-central-1: 322235958271: table/ingestion_flattened_booking_trip_domain_v5/data_set_tripofferrequested_experiments
    pass


def list_cf_stacks(status_filter: list = ["CREATE_COMPLETE"]) -> list:
    """
    list cloudformation stacks
    """
    paginator = cf.get_paginator("list_stacks")
    response = paginator.paginate(
        StackStatusFilter=status_filter
    ).build_full_result()
    return response["StackSummaries"]


def list_cf_stack_ids(status_filter: list = ["CREATE_COMPLETE"]) -> list:
    stacks = list_cf_stacks(status_filter)
    result = [stack["StackId"] for stack in stacks]
    return result


def list_stack_physical_resources(stakc_name: str) -> list:
    response = cf.describe_stack_resources(StackName=stakc_name)
    resources = [resources["PhysicalResourceId"] for resources in response["StackResources"]]
    return resources


def filter_lake_formation_arn(cf_physical_resource: str) -> dict:
    """
    filter the physical resources string and return the role and glue object
    """
    result = {}
    fields = cf_physical_resource.split(":")
    if fields[0] == "LakeFormation-arn":
        result["principal"] = fields[5]
        result["glue_object"] = fields[12]
    return result


def list_database_permissions(principal: str, database: str):
    perm = lf.list_permissions(
        Principal={"DataLakePrincipalIdentifier": principal},
        Database={"Name": database}
    )
    return perm


def list_table_permissions(principal: str, database: str, table: str):
    # table/ingestion_flattened_booking_trip_domain_v5/data_set_tripofferrequested_experiments
    perm = lf.list_permissions(
        Principal={'DataLakePrincipalIdentifier': principal},
        Table={'DatabaseName': database, 'Name': table}
    )
    print(perm)
    return perm


def pretty_json(data: list):
    return json.dumps(data, indent=2)


def main():
    # stacks = list_cf_stacks()
    # print(pretty_json(stacks))
    # stack_ids = list_cf_stack_ids()
    # [
    #     print(f"Resources: {list_stack_physical_resources(stakc_name=name)}")
    #     for name in stack_ids
    # ]
    data = filter_lake_formation_arn(
        cf_physical_resource="LakeFormation-arn:aws:iam::322235958271:role/data-lake-driver-technical-role::arn:aws:glue:eu-central-1:322235958271:table/ingestion_flattened_booking_trip_domain_v5/data_set_tripofferrequested_experiments"
    )
    print(data)
    perm = list_lake_formation_permissions(
        principal="aws:iam::322235958271:role/data-lake-driver-technical-role",
        resource="table/ingestion_flattened_booking_trip_domain_v5/data_set_tripofferrequested_experiments"
    )
    print(perm)
    # return stack_ids


if __name__ == "__main__":
    # print(main())
    main()
