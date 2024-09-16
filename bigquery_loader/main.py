import functions_framework
from urllib.request import urlopen
import zipfile
from io import BytesIO
import pandas as pd
import pandas_gbq
from markupsafe import escape
from google.cloud import storage

BASE_URL = 'https://www.retrosheet.org'
PROJECT_ID = 'baseball-434918'
BUCKET_NAME = 'retrosheets'


def convert_num_to_date(df_series):
    temp_series = df_series.astype('Int64').astype('str')
    temp_series = pd.to_datetime(temp_series, format="%Y%m%d", errors='coerce')
    temp_series = temp_series.dt.date.astype('str').replace('NaT', None)
    return (temp_series)

def write_to_gcs(data, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    with blob.open("wb") as f:
        f.write(data)


@functions_framework.http
def hello_get(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """
    return "Hello World!"

@functions_framework.http
def hello_content(request):
    """Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    content_type = request.headers["content-type"]
    if content_type == "application/json":
        request_json = request.get_json(silent=True)
        if request_json and "name" in request_json:
            name = request_json["name"]
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == "application/octet-stream":
        name = request.data
    elif content_type == "text/plain":
        name = request.data
    elif content_type == "application/x-www-form-urlencoded":
        name = request.form.get("name")
    else:
        raise ValueError(f"Unknown content type: {content_type}")
    return f"Hello {escape(name)}!"


@functions_framework.http
def load_people(request):
    resp = urlopen(f'{BASE_URL}/biofile.zip')
    write_to_gcs(resp.read(), 'biofile.zip')

    myzip = zipfile.ZipFile(BytesIO(resp.read()))
    print(myzip.namelist())
    with myzip as z:
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
            pandas_gbq.to_gbq(df, 'retrosheets.persons', project_id=PROJECT_ID, if_exists='replace')
            return ("People loaded successfully")

@functions_framework.http
def load_ballparks(request):
    resp = urlopen(f'{BASE_URL}/ballparks.zip')
    write_to_gcs(resp.read(), 'ballparks.zip')

    myzip = zipfile.ZipFile(BytesIO(resp.read()))
    print(myzip.namelist())
    with myzip as z:
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
            pandas_gbq.to_gbq(df, 'retrosheets.ballparks', project_id=PROJECT_ID, if_exists='replace')
            return ("Stadiums loaded successfully")

@functions_framework.http
def load_teams(request):
    resp = urlopen(f'{BASE_URL}/teams.zip')
    write_to_gcs(resp.read(), 'teams.zip')

    myzip = zipfile.ZipFile(BytesIO(resp.read()))
    print(myzip.namelist())
    with myzip as z:
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
            pandas_gbq.to_gbq(df, 'retrosheets.teams', project_id=PROJECT_ID, if_exists='replace')
            return ("Teams loaded successfully")