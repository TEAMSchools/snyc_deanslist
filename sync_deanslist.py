#!/user/bin/python3.6

import os
import json
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import zipfile
from gcloud import storage
from deanslist_config import CONFIG

ENDPOINTS = CONFIG['endpoints']
API_KEYS = CONFIG['api_keys']
SAVE_PATH = CONFIG['save_path']
GCLOUD_CREDENTIALS = CONFIG['gcloud_credentials']
GCLOUD_PROJECT_NAME = CONFIG['gcloud_project_name']
GCS_BUCKET_NAME = CONFIG['gcs_bucket_name']

def get_table_data(endpoint_url, endpoint_params, api_keys=API_KEYS):
    """
    gets data at endpoint
    """
    table_data = []
    for k in api_keys:
        payload = {'apikey':k}
        payload.update(endpoint_params)
        r = requests.get(endpoint_url, params=payload)

        r_json = r.json()
        r_data = r_json['data']

        if 'deleted_data' in r_json.keys():
            for d in r_data:
                d['is_deleted'] = 0
            table_data.extend(r_data)

            r_deleted = r_json['deleted_data']
            for d in r_deleted:
                d['is_deleted'] = 1
            table_data.extend(r_deleted)
        else:
            table_data.extend(r_data)

    return table_data

def find_previous_partitions(parameter, stopping_criteria, decrement, endpoint_params, endpoint_url, endpoint_name):
    """
    find all valid historic partitions on PS using count endpoint
    """
    historic_queries = []
    while parameter > stopping_criteria:
        historic_query = {}
        parameter_new = parameter - decrement
        probing_params = {}
        #probing_params['UpdatedSince'] = str(parameter_new)
        probing_params['sdt'] = str(parameter_new)
        probing_params['edt'] = str(parameter_new)
        probing_params['IncludeDeleted'] = 'Y'

        historic_query = {
                'url': endpoint_url,
                'name': endpoint_name,
                'params': probing_params
            }
        historic_queries.append(historic_query)
        parameter = parameter_new

    return historic_queries

def save_file(save_dir, filename, data):
    """
    check if save folder exists (create if not) and save data to specified filepath
        - save_dir
        - filename
        - data
    """
    print('\tSaving to... {}'.format(save_dir))
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    filepath = '{0}/{1}'.format(save_dir, filename)
    with open(filepath, 'w+') as outfile:
        json.dump(data, outfile)

    zipfilepath = filepath.replace('.json','.zip')
    with zipfile.ZipFile(zipfilepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(filepath)

    os.remove(filepath)

def upload_to_gcs(endpoint_name, save_dir, filename, credentials=GCLOUD_CREDENTIALS, project_name=GCLOUD_PROJECT_NAME, bucket_name=GCS_BUCKET_NAME):
    """
    upload file to a Google Cloud Storage blob
        - filepath
        - credentials
        - project
        - bucket_name
    """
    gcs_client = storage.Client(project_name, credentials)
    gcs_bucket = gcs_client.get_bucket(bucket_name)

    filepath = '{0}/{1}'.format(save_dir, filename)
    gcs_path = 'deanslist/{}/{}'.format(endpoint_name, filename)
    gcs_blob = gcs_bucket.blob(gcs_path)

    print('\tUploading to Google Cloud Storage... {}'.format(gcs_blob))
    gcs_blob.upload_from_filename(filepath)

def main():
    if not os.path.isdir(SAVE_PATH):
        os.mkdir(SAVE_PATH)

    ## for each endpoint...
    for i, e in enumerate(ENDPOINTS):
        table_start = datetime.now()

        ## parse variables
        endpoint_name = e['name']
        endpoint_url = e['url']
        endpoint_params = {}

        save_dir = '{0}{1}'.format(SAVE_PATH, endpoint_name)
        filename = '{0}.json'.format(endpoint_name)

        ## if there's a query included...
        if 'params' in e.keys():
            ## format query expression and rename file to include query string
            endpoint_params = e['params']
            query = str(endpoint_params)
            query_filename = ''.join(e for e in query if e.isalnum())
            filename = '{0}_{1}.json'.format(endpoint_name, query_filename)

            ## check if there's already a directory of historical data, and if not...
            if not os.path.isdir(save_dir):
                ## create the directory
                os.mkdir(save_dir)

                ## build list of queries that return valid historical data
                historic_queries = []
                ## TODO: there's got to be a better way to do this
                if endpoint_name == 'behavior':
                    parameter = endpoint_params['UpdatedSince']
                    parameter = datetime.strptime(parameter, '%Y-%m-%d').date()
                    stopping_criteria = datetime.strptime(endpoint_params['sdt'], '%Y-%m-%d').date()
                    decrement = relativedelta(days=1)
                historic_queries = find_previous_partitions(parameter, stopping_criteria, decrement, endpoint_params, endpoint_url, endpoint_name)

                ## extend ENPOINTS list to include `historic_queries`
                ENDPOINTS[i+1:i+1] = historic_queries

        ## download data
        print('GET {0} {1}'.format(endpoint_name, endpoint_params))
        table_data = get_table_data(endpoint_url, endpoint_params)
        row_count = len(table_data)
        print('\t{} rows'.format(row_count))

        if row_count > 0:
            ## save data as JSON file
            save_file(save_dir, filename, table_data)
            filename = filename.replace('.json','.zip')

            ## push JSON file to GCS
            upload_to_gcs(endpoint_name, save_dir, filename)

        table_end = datetime.now()
        table_elapsed = table_end - table_start
        print('\t{0} sync complete!\tElapsed time = {1}'.format(endpoint_name, str(table_elapsed)))

if __name__ == '__main__':
    main()