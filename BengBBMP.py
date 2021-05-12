# sudo pip3 install python-telegram-bot APScheduler==3.7.0 atomicwrites==1.4.0 attrs==20.3.0 
# sudo pip3 install certifi==2020.12.5 chardet==4.0.0 colorama==0.4.4 cowin==0.0.3 fake-useragent==0.1.11 
# sudo pip3 install idna==2.10 iniconfig==1.1.1 packaging==20.9 pluggy==0.13.1 py==1.10.0 pyparsing==2.4.7 
# sudo pip3 install pytest==6.2.3 pytz==2021.1 requests==2.25.1 six==1.15.0 toml==0.10.2 tzlocal==2.1 urllib3==1.26.4

# from apscheduler.schedulers.blocking import BlockingScheduler
import telegram_send
import time
from datetime import datetime
from cowin_api import CoWinAPI
import pandas as pd
import requests

def send_telegram(data,time):
    sesh = data['sessions']
    message = "\nPinCode: " + str(data['pincode']) +"\nName: " + str(data['name']) + "\nDate: "+ str(sesh[0]['date']) + "\nAvailable: " + str(sesh[0]['available_capacity']) + "\n\n\nQueried at :" + str(time)
    print(message)
    mess="Deployed"
    telegram_send.send(conf="~/channel.conf",messages=[message])


def send_notification(data):
  # data1 = (str(data).split('{'))
  for i in data:
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    send_telegram(i,time)

def check_for_vaccine():
    state_id = '16'
    district_id = '294'
    date = datetime.now()
    date = date.strftime("%d-%m-%Y")
    min_age_limit = 18
    available_centers_data = []
    availability = 0
    cowin = CoWinAPI()
    available_centers = cowin.get_availability_by_district(district_id,date,min_age_limit)
    for center in available_centers['centers']:
        _date_capacity = 0
        available_sessions = []
        for session in center['sessions']:
            if(session['available_capacity'] >= 1):
                _date_capacity = 1
                availability = 1
                available_sessions.append(session)
        if(_date_capacity):
            center['sessions'] = available_sessions
            available_centers_data.append(center)
    if availability == 1:
        send_notification(available_centers_data)
    district_id = '265'
    available_centers = cowin.get_availability_by_district(district_id,date,min_age_limit)
    for center in available_centers['centers']:
        _date_capacity = 0
        available_sessions = []
        for session in center['sessions']:
            if(session['available_capacity'] >= 1):
                _date_capacity = 1
                availability = 1
                available_sessions.append(session)
        if(_date_capacity):
            center['sessions'] = available_sessions
            available_centers_data.append(center)
    if availability == 1:
        send_notification(available_centers_data)



def main():
    mess="Deployed"
    telegram_send.send(conf="~/channel.conf",messages=[mess])
    print("Checking centers for vaccination..........")
    while(True):
        check_for_vaccine()
        time.sleep(10)

main()
