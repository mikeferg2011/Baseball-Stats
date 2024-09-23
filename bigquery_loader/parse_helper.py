import pandas as pd
import pandas_gbq
import zipfile
from io import BytesIO
from google.cloud import storage
from abc import ABC, abstractmethod


PROJECT_ID = 'baseball-434918'
BUCKET_NAME = 'retrosheets'


def convert_num_to_date(df_series):
    temp_series = df_series.astype('Int64').astype('str')
    temp_series = pd.to_datetime(temp_series, format="%Y%m%d", errors='coerce')
    temp_series = temp_series.dt.date.astype('str').replace('NaT', None)
    return (temp_series)


class BaseParser(ABC):
    def __init__(self, blob_name, tbl_dest, write_mode):
        self.blob_name = blob_name
        self.tbl_dest = tbl_dest
        self.write_mode = write_mode

    def read_zip_gcs(self):
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(self.blob_name)
        self.zip = zipfile.ZipFile(BytesIO(blob.download_as_string()))

    @abstractmethod
    def process(self):
        pass

    def bq_write(self):
        pandas_gbq.to_gbq(self.df,
                          f'retrosheets.{self.tbl_dest}',
                          project_id=PROJECT_ID,
                          if_exists=self.write_mode
                          )

    def pipeline(self):
        self.read_zip_gcs()
        self.process()
        self.bq_write()


class BallparkParser(BaseParser):

    def __init__(self, blob_name, tbl_dest='ballparks', write_mode='replace'):
        super().__init__(self, blob_name, tbl_dest, write_mode)

    def process(self):
        with self.zip as z:
            # open the csv file in the dataset
            with z.open('ballparks.csv') as f:
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
        self.df = df


class PeopleParser(BaseParser):
    def __init__(self, blob_name, tbl_dest='bios', write_mode='replace'):
        super().__init__(self, blob_name, tbl_dest, write_mode)

    def process(self):
        with self.zip as z:
            # open the csv file in the dataset
            with z.open('biofile0.csv') as f:
                df = pd.read_csv(f)
        col_dict = {
            'id': 'id',
            'lastname': 'last_name',
            'usename': 'first_name',
            'fullname': 'full_name',
            'birthdate': 'birth_date',
            'birthcity': 'birth_city',
            'birthstate': 'birth_state',
            'birthcountry': 'birth_country',
            'deathdate': 'death_date',
            'deathcity': 'death_city',
            'deathstate': 'death_state',
            'deathcountry': 'death_country',
            # 'cemetery', 'cem_city', 'cem_state', 'cem_ctry', 'cem_note',
            'birthname': 'birth_name',
            'altname': 'alt_name',
            'debut_p': 'debut_player',
            'last_p': 'last_player',
            # 'debut_c', 'last_c',
            # 'debut_m', 'last_m',
            # 'debut_u', 'last_u',
            'bats': 'bats',
            'throws': 'throws',
            'height': 'height',
            'weight': 'weight',
            'HOF': 'hof',
        }

        df = df[col_dict.keys()]

        df = df.rename(columns=col_dict)

        df.birth_date = convert_num_to_date(df.birth_date)
        df.death_date = convert_num_to_date(df.death_date)

        df.debut_player = convert_num_to_date(df.debut_player)
        df.last_player = convert_num_to_date(df.last_player)
        self.df = df


class TeamsParser(BaseParser):
    def __init__(self, blob_name, tbl_dest="teams", write_mode="replace"):
        super().__init__(self, blob_name, tbl_dest, write_mode)

    def process(self):
        with self.zip as z:
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
        self.df = df
