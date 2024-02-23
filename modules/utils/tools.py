import json
from datetime import datetime
from typing import List, Dict
import dateparser
import time

def is_json(jstr=None):
    if jstr != None:
        try:
            json_obj = json.loads(jstr)
            return True
        except ValueError as e: 
            return False
        return True
    else:
        return False

def json_loader(jstr=None):
    if is_json(jstr=jstr) == False:
        return None
    else:
        return json.loads(jstr)
    

def process_datetime_string(time_str: str = None):
    if time_str is None:
        return None
    else:
        return dateparser.parse(str(time_str), date_formats=['%d-%m-%Y %H:%M:%S'])

def check_if_time_as_pass_now(time_str: str = None):
    date_parsed = dateparser.parse(str(time_str), date_formats=['%d-%m-%Y %H:%M:%S'])
    time_tz = time.mktime(date_parsed.timetuple())
    time_tz = int(time_tz)
    current_tz = int(time.time())
    if current_tz >= time_tz:
        return True
    else:
        return False
    
def check_if_date_as_pass_now(date_str: str = None):
    date_parsed = dateparser.parse(str(date_str), date_formats=['%d-%m-%Y'])
    present_day = datetime.now()
    if date_parsed.date() < present_day.date():
        return True
    else:
        return False
    
def get_response_datetime_format():
    now = datetime.now()
    return now.strftime("%y%m%d%H%M%S")