import pandas as pd


def convert_num_to_date(df_series):
    temp_series = df_series.astype('Int64').astype('str')
    temp_series = pd.to_datetime(temp_series, format="%Y%m%d", errors='coerce')
    temp_series = temp_series.dt.date.astype('str').replace('NaT', None)
    return (temp_series)


class RetroParser:
    def __init__(self, zip_bytes, zip_type):
        self.zip_bytes = zip_bytes
        self.zip_type = zip_type

    def process_ballparks(self):
        with self.zip_bytes as z:
            # open the csv file in the dataset
            with z.open("ballparks.csv") as f:
                df = pd.read_csv(f)
                df = df.rename(columns={
                    'PARKID': 'park_id',
                    'NAME': 'name',
                    'AKA': 'alt_names',
                    'CITY': 'city',
                    'STATE': 'state',
                    'START': 'start_dt',
                    'END': 'end_dt',
                    'LEAGUE': 'league',
                    'NOTES': 'notes',
                })
                df.start_dt = pd.to_datetime(df.start_dt, format='%m/%d/%Y').astype('str').replace('NaT', None)
                df.end_dt = pd.to_datetime(df.end_dt, format='%m/%d/%Y').astype('str').replace('NaT', None)
        return df

    def process_bios(self):
        with self.zip_bytes as z:
            # open the csv file in the dataset
            with z.open("biofile0.csv") as f:
                df = pd.read_csv(f)
                col_list = [
                    'id', 'lastname', 'usename', 'fullname',
                    'birthdate', 'birthcity', 'birthstate', 'birthcountry',
                    'deathdate', 'deathcity', 'deathstate', 'deathcountry',
                    # 'cemetery', 'cem_city', 'cem_state', 'cem_ctry', 'cem_note',
                    'birthname', 'altname',
                    'debut_p', 'last_p',
                    # 'debut_c', 'last_c',
                    # 'debut_m', 'last_m',
                    # 'debut_u', 'last_u',
                    'bats', 'throws',
                    'height', 'weight',
                    'HOF'
                ]

                df = df[col_list]

                df = df.rename(columns={
                    'id': 'id', 'lastname': 'last_name', 'usename': 'first_name', 'fullname': 'full_name',
                    'birthdate': 'birth_date', 'birthcity': 'birth_city', 'birthstate': 'birth_state', 'birthcountry': 'birth_country',
                    'deathdate': 'death_date', 'deathcity': 'death_city', 'deathstate': 'death_state', 'deathcountry': 'death_country',
                    'birthname': 'birth_name', 'altname': 'alt_name',
                    'debut_p': 'debut_player', 'last_p': 'last_player',
                    'bats': 'bats', 'throws': 'throws',
                    'height': 'height', 'weight': 'weight',
                    'HOF': 'hof',
                })

                df.birth_date = convert_num_to_date(df.birth_date)
                df.death_date = convert_num_to_date(df.death_date)

                df.debut_player = convert_num_to_date(df.debut_player)
                df.last_player = convert_num_to_date(df.last_player)
        return df
    def process_teams(self):
        with self.zip_bytes as z:
            # open the csv file in the dataset
            with z.open("teams.csv") as f:
                df = pd.read_csv(f)
                df = df.rename(columns={
                    'TEAM': 'team_id',
                    'LEAGUE': 'league',
                    'CITY': 'city',
                    'NICKNAME': 'nickname',
                    'FIRST': 'first_year',
                    'LAST': 'last_year',
                })
        return df
    
    def process(self):
        if self.zip_type == 'ballparks':
            df = self.process_ballparks()
            return df, 'replace'
        elif self.zip_type == 'bios':
            df = self.process_bios()
            return df, 'replace'
        elif self.zip_type == 'teams':
            df = self.process_teams()
            return df, 'replace'
        else:
            raise ValueError(f'Unknown file type given. Recieved {self.zip_type}.')
