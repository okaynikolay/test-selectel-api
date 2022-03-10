import requests
import io
import logging
import json
from datetime import datetime, timedelta
import pandas as pd
import time
from airflow.hooks.base import BaseHook
import psycopg2
from dag_etl.queries import CREATE_TABLE, DROP

def connect_to_api(start_date:str, end_date:str):
    url = 'http://localhost:5000/events'
    params = {'start_date':start_date, 'end_date':end_date}
    callback = requests.get(url, params = params)
    js = json.loads(callback.text)
    logging.info('status_code ' +  str(callback.status_code))
    return js

def transform_data(data:list):
    csv_data = io.StringIO()
    for row in data:
        csv_data.write('|'.join((
            row['city'],
            datetime.strptime(row['date'], '%a, %d  %b %Y %H:%M:%S GMT').date().strftime('%Y-%m-%d'),
            row['device'],
            row['user']
        )) + '\n')

    csv_data.seek(0)
    return csv_data

def work_with_db(creds:dict, data:io.StringIO):
    user = creds['user']
    pwd = creds['pwd']
    db = creds['db']
    host = creds['host'] 
    port = creds['port']
    with psycopg2.connect(dbname=db, user=user, password=pwd, host=host, port=port) as conn:
        cur = conn.cursor()
        #cur.execute(DROP)
        cur.execute(CREATE_TABLE)
        cur.copy_from(data, 'events', sep='|', columns=('city','date','device','user'))
        cur.close()
        conn.commit()

def run(creds, start_date, end_date):
    conn = BaseHook.get_connection(creds)
    creds_dict = {'user':conn.login, 'pwd':conn.password, 'db':conn.schema, 
                  'host':conn.host, 'port':conn.port}
    data = connect_to_api(start_date, end_date)
    work_with_db(creds_dict, transform_data(data))

if __name__ == '__main__':
    with open('creds.json', 'r') as f:
        creds = json.load(f)
    total = time.time()
    date_list = [i.strftime('%Y-%m-%d') for i in pd.date_range(datetime.now() - timedelta(30), datetime.now())]
    for start_date, end_date in list(zip(date_list[:-1], date_list[1:])):
        start = time.time()
        data = connect_to_api(start_date, end_date)
        work_with_db(creds, transform_data(data))
        end = time.time()
        diff = round(end - start, 2)
        logging.info("{start_date} complete for {diff} sec".format(start_date = start_date, diff = diff))
    total_diff = round(time.time() - total, 2)
    logging.info("Total is {total_diff}".format(total_diff = total_diff))
