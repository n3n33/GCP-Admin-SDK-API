import pandas as pd
import os
import re

import functions_framework
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import bigquery


SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.readonly']
SERVICE_ACCOUNT_FILE = 'service account key json'
ADMIN_USER = "your google admin email"
project_id = "gcp project"
dataset_id = "bigquery dataset"

def get_google_group_info(scopes, service_account_file, admin_user):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    ).with_subject(ADMIN_USER)

    service = build('admin', 'directory_v1', credentials=credentials)
    # the entire Google Workspace organization associated with the currently authenticated account
    group_json = service.groups().list(customer='my_customer').execute()
    group_tag = 'groups'
    group_list = group_json.get(group_tag, [])
    df = pd.DataFrame(group_list)
    return df

def get_google_group_member_info(scopes, service_account_file, admin_user, group_id):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    ).with_subject(ADMIN_USER)
    
    service = build('admin', 'directory_v1', credentials=credentials)
    member_result = service.members().list(groupKey=f'{group_id}').execute()
    member_tag = 'members'
    member_json = member_result.get(member_tag, [])
    mem_df = pd.DataFrame(member_json)
    return mem_df
    
def df_to_bigquery(dataframe, table_ref):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  
        autodetect=True,                    
    )
    job = client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
    job.result() 
    return "Wrtie ti Bigquery"
    
@functions_framework.http
def main(request):
    group_data = get_google_group_info(SCOPES, SERVICE_ACCOUNT_FILE, ADMIN_USER)
    group_table_id = "google_admin_group_list"
    group_table_ref = f"{project_id}.{dataset_id}.{group_table_id}"
    
    df_to_bigquery(group_data, group_table_ref)

    for id in group_data['id'].tolist():
        member_data = get_google_group_member_info(SCOPES, SERVICE_ACCOUNT_FILE, ADMIN_USER, id)
        member_table_ref = f"{project_id}.{dataset_id}.google_group_{id}_member_list"
        df_to_bigquery(member_data, member_table_ref)
