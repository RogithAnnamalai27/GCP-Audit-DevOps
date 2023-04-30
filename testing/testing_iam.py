from googleapiclient.discovery import build


service = build('cloudresourcemanager','v3')
project = "rogith-384802"
policy_request = service.projects().getIamPolicy(resource=f'projects/{project}', body={})
policy_response = policy_request.execute()

user_with_roles = {}

for binding in policy_response['bindings']:
    for member in binding['members']:
        if member in list(user_with_roles.keys()):
            user_with_roles[member].append(binding['role'])
        else:
            user_with_roles[member]= [str(binding['role'])]

for users in user_with_roles.keys():
    user = users.split(':')
    print(f"User type : {user[0]}\t User ID : {user[1]}\t Roles : {','.join(user_with_roles[users])}")
