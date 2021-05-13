# This is a sample Python script.
import datetime
import json
import random
import socket
import struct
import time
from copy import deepcopy

import pandas as pd
import requests
from pygame import mixer


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def check_availability(today):
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    browser_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    for id_ in [294, 265]:
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={id_}&date={today}"
        # print(url)
        get_availability(url, browser_header)
    # print(URL)
    # Use a breakpoint in the code line below to debug your script.
    time.sleep(15)


def get_availability(url, browser_header):
    response = requests.get(url, headers=browser_header)
    final_df = None
    if response.ok and ('centers' in json.loads(response.text)):
        resp_json = json.loads(response.text)['centers']
        if resp_json is not None:
            df = pd.DataFrame(resp_json)
            if len(df):
                df = df.explode("sessions")
                df['min_age_limit'] = df.sessions.apply(lambda x: x['min_age_limit'])
                df['vaccine'] = df.sessions.apply(lambda x: x['vaccine'])
                df['available_capacity'] = df.sessions.apply(lambda x: x['available_capacity'])
                df['date'] = df.sessions.apply(lambda x: x['date'])
                df = df[["date", "available_capacity", "vaccine", "min_age_limit", "pincode", "name", "state_name",
                         "district_name", "block_name", "fee_type"]]
                if final_df is not None:
                    final_df = pd.concat([final_df, df])
                else:
                    final_df = deepcopy(df)
    else:
        raise Exception(response.status_code)

    # print(final_df[["date", "available_capacity","min_age_limit","name"]])
    if final_df is not None:
        # final_df.loc[len(final_df.index)] = ['2021-12-10', 2, 'covishied', 18, '560016', 'KR Puram hospital',
        #                                      'karnataka',
        #                                      'bangaluru', 'asdf', 'free']
        # print(final_df[(final_df['min_age_limit'] == 18) & (final_df['available_capacity'] > 0)][
        #       ['date', 'min_age_limit', 'available_capacity']])
        alarm_df = final_df[(final_df['min_age_limit'] == 18) & (final_df['available_capacity'] > 10)]
        if alarm_df.shape[0] > 0:
            print("available vaccine details")
            print(alarm_df[["date", "available_capacity", "min_age_limit", "name","pincode"]])
            # Starting the mixer
            mixer.init()

            # Loading the song
            mixer.music.load("covid_alarm.mp3")

            # Setting the volume
            mixer.music.set_volume(0.7)

            # Start playing the song
            for i in range(5):
                mixer.music.play()
                time.sleep(5)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        dt = str(datetime.date.today())
        original_date = datetime.datetime.strptime(dt, '%Y-%m-%d')
        today = original_date.strftime("%d-%m-%Y")
        check_availability(today)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
