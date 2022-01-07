#!/usr/local/bin/python3

##############################
#Auther Susanta Kumar Sahoo
##############################


import os
import requests
import json
import argparse

from datetime import datetime, timedelta

# Time frame to check the PD Oncall Guy, can be changed based on need
day_start = '  01:00:00' #keep the blank space
day_end = ' 23:00:00' #keep the blank space



Inventory = {}

my_date = datetime.now()
last_hour_date_time = datetime.now() - timedelta(hours = 24)



since_start = my_date.strftime('%Y-%m-%d') + day_start
until_end = my_date.strftime('%Y-%m-%d') + day_end

class PagerdutyClient:
    def __init__(self, token):
        self.pagerduty_token = token

    @staticmethod
    def _url():
        return 'https://api.pagerduty.com/'

    def call_api(self, resource_path, params=None):
        headers = {
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Authorization': 'Token token={token}'.format(token=self.pagerduty_token)
        }
        url = self._url() + resource_path + '?limit=5000'
        response_data = requests.get(url, headers=headers, params=params)
        return json.loads(response_data.text)

    def get_user(self,resource_path,ID,params=None):
        headers = {
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Authorization': 'Token token={token}'.format(token=self.pagerduty_token)
        }
        url = self._url() + resource_path + '/' + ID + '?since=' + str(since_start) + '&until=' + str(until_end) + '&overflow=true'
        ##https://api.pagerduty.com/schedules/PS08AXT?since=2022-01-04 17:19:34.249226&until=2022-01-05 17:19:34.249222&overflow=true
        response_data = requests.get(url, headers=headers, params=params)
        ref =  response_data,json.loads(response_data.text)
        str_temp = ''
        for list in  (ref[1]['schedule']['final_schedule']['rendered_schedule_entries']):
            str_temp = str_temp + list['user']['summary'] + '[StartTime:' + list['start'] + ', EndTime:' + list['end'] + '] '

        return str_temp

    def get_pd_inventory(self, type):
        response = self.call_api(type)
        for list in response[type]: #print (list['id'],list['summary'],list['users'])
            Inventory[list['id']] = list['summary'].strip()

    def find_schedule(self,type,Summary):
        for key in Inventory:
            if Summary == Inventory[key]:
                oncall_guys = self.get_user(type, key)
                FinalRecord =  "OnCallScheduleName: [" + Summary  + '], OnCallGuys: '+ oncall_guys
                print (FinalRecord)
                break

    def full_list(self):
        for k, v in sorted(Inventory.items(), key=lambda x: x[1].lower()):
            print((k, v))

    def help(self):
        print ("-h|--help ")

# +--------------------+
#     MAIN PROGRAM
# +--------------------+
def main():
    pd = PagerdutyClient(os.getenv('PD_TOKEN'))
    pd.get_pd_inventory('schedules')
    if args.list:
        pd.full_list()
    if args.schedule:
        pd.find_schedule('schedules',args.schedule.strip())
    else:
        lmodel = False


if __name__ == '__main__':
    helptitle = "Menue based SRE automation script ..."
    parser = argparse.ArgumentParser(description=helptitle)
    parser.add_argument('-l', action='store_const', dest='list',const='list',help='Give the full list of Schedule avaiable in PD in [ID,NAME] format, pass the NAME into -s argument')
    parser.add_argument("-s", dest='schedule', action='store', help="Get the full list of SCHEDULE ./PageDutyInfo.py -l, keep the argument to -s inside the double/single quote", default=False)

    parser.set_defaults(verbose=False)
    args = parser.parse_args()
    main()
