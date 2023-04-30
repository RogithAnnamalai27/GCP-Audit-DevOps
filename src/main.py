from utils import iam_policies
from utils import gcp_projects
from utils import sql_users

from googleapiclient.discovery import build
import xlsxwriter


########## Get GCP projects list ##########
list_project_file_path = "artifacts/GCP_projects.xlsx"      #Update file path where you need list of GCP users

# To Fetch GCP projects to which the credentials have access
gcp_projects.generate_gcp_projects_list(list_project_file_path)
# To get the list of GCP Projects in a List
projects_list = gcp_projects.get_gcp_projects(list_project_file_path)



########## GCP IAM users list ##########
gcp_user_file_path = "artifacts/GCP_users.xlsx"             #Update file path which contains the list of GCP Project IDs

# To fetch list of IAM principals from all the projects mentioned in the projects_list
iam_policies.list_users_excel(projects_list,gcp_user_file_path)


########## Cloud SQL users list ##########
sql_users.get_sql_users_excel(projects_list)


