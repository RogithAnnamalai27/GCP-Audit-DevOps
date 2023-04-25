from googleapiclient.discovery import build


def get_gcp_projects_list(org_id):
    #org_id = ""
    service = build('cloudresourcemanager','v3')
    policy_request = service.projects().list(parent=f"organizations/{org_id}")
    policy_response = policy_request.execute()

    print(policy_request)

