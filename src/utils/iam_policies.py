from googleapiclient.discovery import build

import xlsxwriter
import os


## Fetch the list of users, serviceAccounts and groups who have access to the projects
def list_users_excel(projects_list,file_path):

    print("Running scripts to generate the list of IAM principals for GCP projects")

    service = build('cloudresourcemanager','v3')
    # Creating a workbook for IAM Audit
    workbook = xlsxwriter.Workbook(file_path)

    ## Traversing through all the projects
    for project in projects_list:
        print("Current project : "+project)
        row=0
        ## Fetch IAM Policies via Cloud Resource Manager API for the mentioned project
        policy_request = service.projects().getIamPolicy(resource=f'projects/{project}', body={})
        policy_response = policy_request.execute()
        ## Creating a sheet with name = Project ID
        worksheet = workbook.add_worksheet(project)

        ## Fetching the user ID and roles from each response
        users_with_roles = get_users_with_roles(policy_response)
        
        ## Adding a title for each column
        worksheet.write(row,0,'User type')
        worksheet.write(row,1,'ID')
        worksheet.write(row,2,'Roles Assigned')
        row += 1

        for users in users_with_roles.keys():
            user = users.split(':')
            roles = ', '.join(users_with_roles[users])
            ## Writing user details to each row
            worksheet.write(row,0,user[0])
            worksheet.write(row,1,user[1])
            worksheet.write(row,2,roles)
            row += 1
        print("\tStatus : Completed")

    ## Closing the open workbook to save the file
    workbook.close()
    print(f"Excel with list of GCP IAM principals for all projects is created at {file_path}\n")


## Fetch list of IAM principals with roles assigned
def get_users_with_roles(iam_response):

    users_with_roles = {}

    ## Traversing through the response and fetching the users with roles assigned
    ## Dictionary with user ID and roles assigned to it will be created 
    for binding in iam_response['bindings']:
        for member in binding['members']:
            if member in list(users_with_roles.keys()):
                users_with_roles[member].append(binding['role'])
            else:
                users_with_roles[member]= [str(binding['role'])]

    ## Return the dicctionary of users with roles assigned
    return users_with_roles