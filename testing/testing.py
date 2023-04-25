from googleapiclient.discovery import build


project_id = "rogith-384802"
row = 0
column = 0
def testing_vm():
        
    service = build('compute', 'v1')
    request = service.instances().aggregatedList(project=project_id)

    while request is not None:
        response = request.execute()
        list_instance = response.get('items', {})
        for instances in list_instance.values():
            for instance in instances.get('instances', []):
                disk_info = instance['disks'][0]
                os = ""
                if 'windows' in str(disk_info['licenses']):
                    os = "windows"
                else:
                    os = "linux"
                print(str(instance['id'])+"\t"+os+"\n")
        request = service.instances().aggregatedList_next(previous_request=request, previous_response=response)

def vm_instances_list():

    project_id = "rogith-384802"
    zone = ""
    service = build('compute', 'v1')
    request = service.instances().list(project=project_id, zone=zone)
    while request is not None:
        response = request.execute()

        for instance in response['items']:
            # TODO: Change code below to process each `instance` resource:
            print(instance)

        request = service.instances().list_next(previous_request=request, previous_response=response)

vm_instances_list()