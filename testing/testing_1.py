import google.cloud.logging
from google.cloud.logging import DESCENDING


# Set the service account key file path and project ID 
# SERVICE_ACCOUNT_FILE = 'artifacts/rogith_sa_key.json' 

project_id = 'rogith-384802' 
# Set the VM instance name and log filter 
INSTANCE_NAME = 'instance-2' 
LOG_FILTER = f'resource.type="gce_instance" AND resource.labels.instance_id = "5465319859794148330" AND protoPayload.type = "type.googleapis.com/google.cloud.audit.AuditLog"' 

client = google.cloud.logging.Client(project=project_id)
for entry in client.list_entries(order_by=DESCENDING, filter_=LOG_FILTER):
    print(entry)
    print()
