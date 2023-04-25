from googleapiclient import discovery
import xlsxwriter

def get_sql_users_excel(project_id):

    service = discovery.build('sqladmin', 'v1beta4')
    instance_request = service.instances().list(project=project_id)
    workbook = xlsxwriter.Workbook("artifacts/Cloud_SQL_users.xlsx")

    instances_dict = get_list_sql_instances(project_id)

    for instance_type in list(instances_dict.keys()):
        row = 0
        column = 0
        #instance_type = "MYSQL"
        worksheet = workbook.add_worksheet(instance_type)

        for instance in instances_dict[instance_type]:
            #print(instance)
            row =0
            worksheet.write(row,column,instance)
            row += 1
            list_users = get_list_users(project_id,instance)
            
            for user in list_users:
                worksheet.write(row,column,user)
                row += 1
            column += 1

    workbook.close()

def get_list_sql_instances(project_id):

    instances = {}
    service = discovery.build('sqladmin', 'v1beta4')
    request = service.instances().list(project=project_id)

    while request is not None:
        response = request.execute()

        for database_instance in response['items']:
            #print(database_instance.get('name',[]),database_instance.get('databaseVersion',[]))
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
    return instances

def get_list_users(project_id,instance_name):

    users = []
    service = discovery.build('sqladmin', 'v1beta4')
    request = service.users().list(project=project_id, instance=instance_name)
    response = request.execute()
    
    for item in response.get('items'):
        users.append(item.get('name'))

    return users

#print(get_list_sql_instances("rogith-384802"))
#print(get_list_users("rogith-384802","testing-audit"))