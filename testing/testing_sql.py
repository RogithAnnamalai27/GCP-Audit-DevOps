
from pprint import pprint
from googleapiclient import discovery

service = discovery.build('sqladmin', 'v1beta4')

# Project ID of the project that contains the instance.
project_id = "rogith-384802"  # TODO: Update placeholder value.

# Database instance ID. This does not include the project ID.
instance = 'testing-audit'  # TODO: Update placeholder value.

request = service.users().list(project=project_id, instance=instance)
response = request.execute()

# TODO: Change code below to process the `response` dict:
pprint(response)


service_i = discovery.build('sqladmin', 'v1beta4')


request = service_i.instances().list(project=project_id)
while request is not None:
    response = request.execute()

    for database_instance in response['items']:
        # TODO: Change code below to process each `database_instance` resource:
        pprint(database_instance)

    request = service.instances().list_next(previous_request=request, previous_response=response)

