from googleapiclient.discovery import build
import xlsxwriter


def list_users_excel(project_id):

    row=0
    service = build('cloudresourcemanager','v3')
    policy_request = service.projects().getIamPolicy(resource=f'projects/{project_id}', body={})
    policy_response = policy_request.execute()
    workbook = xlsxwriter.Workbook("artifacts/GCP_users.xlsx")
    worksheet = workbook.add_worksheet("IAM_users")

    for binding in policy_response['bindings']:
        user = binding['members'][0]
        user = user.split(':')

        if row == 0:
            worksheet.write(row,0,'User type')
            worksheet.write(row,1,'ID')
        else:
            worksheet.write(row,0,user[0])
            worksheet.write(row,1,user[1])
        row += 1

    workbook.close()
