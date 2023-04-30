from googleapiclient.discovery import build
import os

def list_linux_vm():
    project_id = "rogith-384802"
    service = build('compute', 'v1')
    request = service.instances().aggregatedList(project=project_id)

    while request is not None:
        response = request.execute()
        list_instance = response.get('items', {})
        for instances in list_instance.values():
            for instance in instances.get('instances', []):
                disk_info = instance['disks'][0]
                if "windows" not in str(disk_info['licenses']):
                    print()
                print(disk_info['licenses'])
        request = service.instances().aggregatedList_next(previous_request=request, previous_response=response)
