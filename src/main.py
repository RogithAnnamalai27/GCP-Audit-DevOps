from utils import iam_policies
from utils import compute_engine_users
from utils import sql_users

from googleapiclient.discovery import build
import os



project_id = "rogith-384802"

# GCP IAM users list
iam_policies.list_users_excel(project_id)

# Compute Engine users list
#windows_worksheet = workbook.add_worksheet("Windows_users")
#linux_worksheet = workbook.add_worksheet("Linux_users")
#compute_engine_users.list_instance_users(project_id,windows_worksheet,linux_worksheet)

# GCP IAM users list
sql_users.get_sql_users_excel(project_id)

