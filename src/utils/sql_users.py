from googleapiclient import discovery
import xlsxwriter
import os


## Fetch list of users of all Cloud SQL instance from all the projects
def get_sql_users_excel(projects_list):

    print("Running scripts to generate the list of Cloud SQL users of each instance type for GCP projects")

    # Creating workbook for all types of instance
    POSTGRES_workbook = xlsxwriter.Workbook(f"artifacts/POSTGRES_users.xlsx")
    MYSQL_workbook = xlsxwriter.Workbook(f"artifacts/MYSQL_users.xlsx")
    SQLSERVER_workbook = xlsxwriter.Workbook(f"artifacts/SQLSERVER_users.xlsx")
    
    service = discovery.build('sqladmin', 'v1beta4')

    # Traversing through all the projects
    for project in projects_list:
        print("Current project : "+project)
        ## Fetching the list of instances from the mentioned
        flag = 0
        ## Will return a dict with instance type as key and lsit of instance name as value
        instances_dict = get_list_sql_instances(str(project))

        ## Traversing through instance types
        for instance_type in list(instances_dict.keys()):
            ## Creating worksheets in respective workbook based on the instance type from previous step
            if instance_type == "POSTGRES":
                worksheet = POSTGRES_workbook.add_worksheet(project)
            elif instance_type == "MYSQL":
                worksheet = MYSQL_workbook.add_worksheet(project)
            else:
                worksheet = SQLSERVER_workbook.add_worksheet(project)

            row = 0
            column = 0         
            ## Traversing through instance names of mentioned instance type
            for instance in instances_dict[instance_type]:
                print("\tInstance Name : "+instance)
                row = 0
                flag = 1
                ## Adding column title as instance name
                worksheet.write(row,column,instance)
                row += 1
                ## Fetching the list of users for the mentioned instance
                list_users = get_list_users(project,instance)
                ## If Instance is Not Running, result will be None
                if list_users is None: 
                    continue
                else:
                    flag = 1

                ## Writing list of users under the respective instance name
                for user in list_users:
                    worksheet.write(row,column,user)
                    row += 1
                column += 1
        if flag == 0 :
            print("\tNo instances found in the mentioned project")
            

    POSTGRES_workbook.close()
    MYSQL_workbook.close()
    SQLSERVER_workbook.close()
    print(f"Excel with list of GCP IAM principals for all projects is created inside folder name - 'artifacts'\n")


## Fetch the list of instance name under mentioned GCP Project
def get_list_sql_instances(project_id):

    instances = {}
    service = discovery.build('sqladmin', 'v1beta4')
    request = service.instances().list(project=project_id)

    while request is not None:
        response = request.execute()

        if response is not None and response != {}:
            ## Creating a dictionary with key as instance type and value as list of instances name
            for database_instance in response['items']:
                if 'POSTGRES' in str(database_instance.get('databaseVersion',[])):
                    if 'POSTGRES' in list(instances.keys()):
                        instances['POSTGRES'].append(database_instance.get('name',[]))
                    else:
                        instances['POSTGRES']= [str(database_instance.get('name',[]))]
                elif 'MYSQL' in str(database_instance.get('databaseVersion',[])):
                    if 'MYSQL'  in list(instances.keys()):
                        instances['MYSQL'].append(database_instance.get('name',[]))
                    else:
                        instances['MYSQL']= [str(database_instance.get('name',[]))]
                else:
                    if 'SQLSERVER'  in list(instances.keys()):
                        instances['SQLSERVER'].append(database_instance.get('name',[]))
                    else:
                        instances['SQLSERVER']= [str(database_instance.get('name',[]))]

        request = service.instances().list_next(previous_request=request, previous_response=response)
    ## Return the Dict of instance details
    return instances


## Fetch of users from mentioned instance name
def get_list_users(project_id,instance_name):

    users = []
    service = discovery.build('sqladmin', 'v1beta4')
    request = service.users().list(project=project_id, instance=instance_name)
    try:
        response = request.execute()
    except:
        ## Any error from response
        print(f"\t\tInstance {instance_name} is Not Running")
        return None
    
    for item in response.get('items'):
        users.append(item.get('name'))

    return users
