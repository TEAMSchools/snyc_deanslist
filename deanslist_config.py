from datetime import datetime, timedelta
import pytz

save_path = ''
tz = pytz.timezone('')
today = datetime.now(tz).date()
today_str = today.strftime('%Y-%m-%d')
yesterday_str = today - timedelta(days=1)
yesterday_str = yesterday_str.strftime('%Y-%m-%d')

"""
DeansList variables
"""
base_url = ''
api_keys = [
        '',
    ]

endpoints = [
        ## FLAT JSON - PARAMETERS ##
        {'endpoint':'/api/beta/export/get-behavior-data.php',
         'name':'behavior',
         'params':{'sdt':'2016-07-01', 'edt':yesterday_str, 'UpdatedSince':yesterday_str, 'IncludeDeleted':'Y'}},
        ## FLAT JSON - NO PARAMETERS ##
        {'endpoint':'/api/v1/referrals', 'name':'referrals'},
        {'endpoint':'/api/beta/export/get-comm-data.php', 'name':'communication'},
        {'endpoint':'/api/v1/followups', 'name':'followups'},
        {'endpoint':'/api/beta/export/get-roster-assignments.php', 'name':'roster_assignments'},
        {'endpoint':'/api/v1/lists', 'name':'lists'},
        {'endpoint':'/api/v1/rosters', 'name':'rosters_all'},
        {'endpoint':'/api/beta/export/get-users.php', 'name':'users'},
        ## CONTAIN NESTED JSON ##
        {'endpoint':'/api/v1/incidents', 'name':'incidents'},
        # ## UNUSED ##
        # {'endpoint':'/api/beta/export/get-homework-data.php', 'name':'homework', 'array_cols':[]},
        # {'endpoint':'/api/v1/suspensions', 'name':'suspensions', 'nested':1, 'array_cols':[]},
        # {'endpoint':'/api/v1/students', 'name':'students', 'nested':0},
        # {'endpoint':'/api/v1/daily-attendance', 'name':'daily_attendance', 'nested':0},
        # {'endpoint':'/api/v1/class-attendance', 'name':'class_attendance', 'nested':0},
        # {'endpoint':'/api/v1/terms', 'name':'terms', 'nested':1},
        # {'endpoint':'/api/beta/bank/get-bank-book.php', 'name':'points_bank', 'nested':1},
        # {'endpoint':'/api/v1/lists/{ListID}', 'name':'list_sessions_all', 'nested':1},
        # {'endpoint':'/api/v1/lists/{ListID}/{SessionID}', 'name':'list_sessions_id', 'nested':1},
        # {'endpoint':'/api/v1/lists/{ListID}/{SessionDate}', 'name':'list_sessions_date', 'nested':1},
        # {'endpoint':'/api/v1/rosters/(RosterID)', 'name':'rosters_single', 'nested':1},
    ]

"""
all together now!
"""
CONFIG = {
        'base_url': base_url,
        'api_keys': api_keys,
        'endpoints': endpoints,
        'save_path': save_path
    }
