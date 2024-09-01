import mysql.connector
import pandas as pd
import os
from sqlalchemy import create_engine

directory = os.fsencode('D:\GitHub\Baseball-Stats\event_files')
engine = create_engine('mysql+mysqlconnector://root:ferg@localhost:3306/mlb', echo=False)

#Team Roster Files
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".ROS"):
         #print(os.path.join(directory, filename))
         print(filename)
         df = pd.read_csv('D:/GitHub/Baseball-Stats/event_files/'+filename,
                          header = None,
                          names = ['playerid', 'last_name', 'first_name', 'hit_hand', 'throw_hand', 'teamid', 'pos'])
         df['team_year'] = filename[:-4]
         df['year'] = filename[3:7]
         df.to_sql(name='roster_year', con=engine, if_exists = 'append', index=False)
         continue
     else:
         continue

#Team-Year file
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.startswith('TEAM'):
         #print(os.path.join(directory, filename))
         print(filename)
         df = pd.read_csv('D:/GitHub/Baseball-Stats/event_files/'+filename,
                          header = None,
                          names = ['teamid', 'league', 'city', 'team_name'])
         df['team_year'] = df['teamid'] + filename[-4:]
         df['year'] = filename[-4:]
         df.to_sql(name='team_year', con=engine, if_exists = 'append', index=False)
         continue
     else:
         continue

# Event files
# https://www.retrosheet.org/datause.txt
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".csv"):
         #print(os.path.join(directory, filename))
         print(filename)
         df = pd.read_csv('D:/GitHub/Baseball-Stats/event_files/'+filename,
                          header = None,
                          names = ['gameid','vis_team','inning','batting_team',
                                   'outs','balls','strikes','vis_score','home_score',
                                   'resbatter','resbatterhand','respitcher','respitcherhand',
                                   'firstrunner','secondrunner','thirdrunner',
                                   'event_text','leadoff','pinchhit','def_pos','lineup_pos',
                                   'event_type','batter_event_flag','ab_flag','hit_value',
                                   'sh_flag','sf_flag','outs_on_play','rbi_on_play',
                                   'wildpitch_flag','passedball_flag','num_errors',
                                   'batter_dest','first_dest','second_dest','third_dest'])
         df['home_team'] = filename[4:7]        
         df['year'] = filename[0:4]
         df['ds'] = pd.to_datetime(df['gameid'].str[3:11], format='%Y%m%d')
         df['game_num'] = pd.to_numeric(df['gameid'].str[-1]) +1
         df.to_sql(name='game_events', con=engine, if_exists = 'append', index=False)
         continue
     else:
         continue

# Player ID to name & debut (https://www.retrosheet.org/retroID.htm)
df = pd.read_csv('D:/GitHub/Baseball-Stats/players.csv')
df['player_debut'] = pd.to_datetime(df['player_debut'], format='%m/%d/%Y', errors = 'coerce')
df['mgr_debut'] = pd.to_datetime(df['mgr_debut'], format='%m/%d/%Y', errors = 'coerce')
df['coach_debut'] = pd.to_datetime(df['coach_debut'], format='%m/%d/%Y', errors = 'coerce')
df['ump_debut'] = pd.to_datetime(df['ump_debut'], format='%m/%d/%Y', errors = 'coerce')
df.to_sql(name='players', con=engine, if_exists = 'replace', index=False)

# Park info (https://www.retrosheet.org/parkcode.txt)
df = pd.read_csv('D:/GitHub/Baseball-Stats/parks.csv')
df['START'] = pd.to_datetime(df['START'], format='%m/%d/%Y', errors = 'coerce')
df['END'] = pd.to_datetime(df['END'], format='%m/%d/%Y', errors = 'coerce')
df.to_sql(name='parks', con=engine, if_exists = 'replace', index=False)

# Park info (https://www.retrosheet.org/parkcode.txt)
df = pd.read_csv('D:/GitHub/Baseball-Stats/event_type_map.csv')
df.to_sql(name='event_type_lkp', con=engine, if_exists = 'replace', index=False)