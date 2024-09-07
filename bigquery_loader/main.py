import functions_framework
from urllib.request import urlopen
import zipfile
from io import BytesIO
import pandas as pd
import pandas_gbq

BASE_URL = 'https://www.retrosheet.org'
PROJECT_ID = 'baseball-434918'

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
def load_people(request):
    resp = urlopen(f'{BASE_URL}/biofile.zip')
    myzip = zipfile.ZipFile(BytesIO(resp.read()))
    print(myzip.namelist())
    with myzip as z:
        # open the csv file in the dataset
        with z.open("biofile0.csv") as f:
            train = pd.read_csv(f)
            print(train.head())
            pandas_gbq.to_gbq(train, 'retrosheets.biofile0', project_id=PROJECT_ID, if_exists='replace')