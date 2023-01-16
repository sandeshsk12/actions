import pandas as pd 
import gspread as gs
import numpy as np
from gspread_dataframe import set_with_dataframe
from datetime import date
today = date.today()
from shroomdk import ShroomDK
import tweepy

sdk = ShroomDK("00dba474-bd21-4d4d-a9b9-c5eaa08aac33")
gc = gs.service_account(filename='/media/sandesh/7b4515cf-7277-44bc-a068-425d5c6990f9/crypto/dummy/credentials.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1wmVhR3GYJIcAvKR1j_XawVwbTI0Vmi_8K5Bv4vGGHF8/edit?usp=sharing')
ws = sh.worksheet('dao_details')
df = pd.DataFrame(ws.get_all_records())


ws = sh.worksheet('dao_details')
dao_details = pd.DataFrame(ws.get_all_records())
dao_list=dao_details['twitter handle'].apply(lambda x: x.replace('https://twitter.com/',''))


ws = sh.worksheet('twitter_log')
twitter_log=pd.DataFrame(ws.get_all_records())
auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAEKQiwEAAAAACaGFqOl1LhYAkmTGKqN9%2FrrFNqc%3D47Yh8KbJE0crZ8bUtE7AS7h88iT5gJq9H3cy63zWZqGmf8DwJJ")
api = tweepy.API(auth)
for dao in dao_list:
    user_dict=(api.get_user(screen_name=dao))._json
    twitter_today=pd.DataFrame([[today,user_dict['name'],user_dict['followers_count'],user_dict['friends_count']]],columns=['Date','Dao Name','Followers','Following'])
    twitter_log=pd.concat([twitter_log,twitter_today])
df = pd.DataFrame(ws.get_all_records())
set_with_dataframe(ws, twitter_log)
