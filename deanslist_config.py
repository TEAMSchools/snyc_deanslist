from datetime import datetime, timedelta
import pytz
from oauth2client.service_account import ServiceAccountCredentials

api_keys = [
        '',
    ]

tz = pytz.timezone('')
today = datetime.now(tz).date()
today_str = today.strftime('%Y-%m-%d')
yesterday_str = today - timedelta(days=1)
yesterday_str = yesterday_str.strftime('%Y-%m-%d')

endpoints = [
        ## FLAT JSON - PARAMETERS ##
        {'url':'https://kippnj.deanslistsoftware.com/api/beta/export/get-behavior-data.php',
         'name':'behavior',
         'params':{'sdt':'2016-07-01', 'edt':yesterday_str, 'UpdatedSince':yesterday_str, 'IncludeDeleted':'Y'}},

        ## FLAT JSON - NO PARAMETERS ##
        {'url':'https://kippnj.deanslistsoftware.com/api/v1/referrals', 'name':'referrals'},
        {'url':'https://kippnj.deanslistsoftware.com/api/beta/export/get-comm-data.php', 'name':'communication'},
        {'url':'https://kippnj.deanslistsoftware.com/api/v1/followups', 'name':'followups'},
        {'url':'https://kippnj.deanslistsoftware.com/api/beta/export/get-roster-assignments.php', 'name':'roster_assignments'},
        {'url':'https://kippnj.deanslistsoftware.com/api/v1/lists', 'name':'lists'},
        {'url':'https://kippnj.deanslistsoftware.com/api/v1/rosters', 'name':'rosters_all'},
        {'url':'https://kippnj.deanslistsoftware.com/api/beta/export/get-users.php', 'name':'users'},

        ## CONTAIN NESTED JSON ##
        {'url':'https://kippnj.deanslistsoftware.com/api/v1/incidents', 'name':'incidents'},


        # ## UNUSED ##
        # {'url':'https://kippnj.deanslistsoftware.com/api/beta/export/get-homework-data.php', 'name':'homework', 'array_cols':[]},
        # {'url':'https://kippnj.deanslistsoftware.com/api/v1/suspensions', 'name':'suspensions', 'nested':1, 'array_cols':[]},
        # {'url':'https://kippnj.deanslistsoftware.com/api/v1/students', 'name':'students', 'nested':0},
        # {'url':'https://kippnj.deanslistsoftware.com/api/v1/daily-attendance', 'name':'daily_attendance', 'nested':0},
        # {'url':'https://kippnj.deanslistsoftware.com/api/v1/class-attendance', 'name':'class_attendance', 'nested':0},
        # {'url':'https://kippnj.deanslistsoftware.com/api/v1/terms', 'name':'terms', 'nested':1},
        # {'url':'https://kippnj.deanslistsoftware.com/api/beta/bank/get-bank-book.php', 'name':'points_bank', 'nested':1},
        # {'url':'https://kippnj.deanslistsoftware.com/api/v1/lists/{ListID}', 'name':'list_sessions_all', 'nested':1},
        # {'url':'https://kippnj.deanslistsoftware.com/api/v1/lists/{ListID}/{SessionID}', 'name':'list_sessions_id', 'nested':1},
        # {'url':'https://kippnj.deanslistsoftware.com/api/v1/lists/{ListID}/{SessionDate}', 'name':'list_sessions_date', 'nested':1},
        # {'url':'https://kippnj.deanslistsoftware.com/api/v1/rosters/(RosterID)', 'name':'rosters_single', 'nested':1},
    ]

"""
GCS config variables
    - gcloud_keyfile            /path/to/keyfile.json for API access to GCloud
    - gcloud_project_name       name of the GCloud project that your bucket lives under
    - gcs_bucket_name           name of the bucket where you are storing this data
"""
save_path = ''
gcloud_keyfile = ''
gcloud_project_name = ''
gcs_bucket_name = ''
gcloud_credentials = ServiceAccountCredentials.from_json_keyfile_name(gcloud_keyfile)

"""
all together now!
"""
CONFIG = {
        'api_keys': api_keys,
        'endpoints': endpoints,
        'save_path': save_path,
        'gcloud_credentials': gcloud_credentials,
        'gcloud_project_name': gcloud_project_name,
        'gcs_bucket_name': gcs_bucket_name
    }
