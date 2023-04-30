from googleapiclient import discovery

project_id = "rogith-384802"

service = discovery.build('sqladmin', 'v1beta4')
request = service.instances().list(project=project_id)

while request is not None:
    response = request.execute()

    if response is not None and response != {}:
        for database_instance in response['items']:
            if "post" in database_instance['name'] :
                print(database_instance['databaseVersion'],database_instance['state'])

    request = service.instances().list_next(previous_request=request, previous_response=response)