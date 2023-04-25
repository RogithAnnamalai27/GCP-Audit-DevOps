from googleapiclient.discovery import build

def list_instance_users(project_id,windows_worksheet,linux_worksheet):

    row = 0
    column = 0
    
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
                    worksheet = windows_worksheet
                else:
                    worksheet = linux_worksheet
                list_users = instance_users(str(instance['id']))
        request = service.instances().aggregatedList_next(previous_request=request, previous_response=response)

def instance_users(instance_id,worksheet):
    
    return 0