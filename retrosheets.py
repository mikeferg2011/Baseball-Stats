from urllib.request import urlretrieve, urlopen
import zipfile
from io import BytesIO
import pandas as pd
import pandas_gbq

BASE_URL = 'https://www.retrosheet.org'

def fetch_people():
    urlretrieve(f'{BASE_URL}/biofile.zip', 'test_player.zip')

def parse_zip():
    root = zipfile.Path('test_player.zip')
    print(root)
    print(root.is_dir())
    print(list(root.iterdir()))

def fetch_people_2():
    resp = urlopen(f'{BASE_URL}/biofile.zip')
    myzip = zipfile.ZipFile(BytesIO(resp.read()))
    print(myzip.namelist())
    with myzip as z:
        # open the csv file in the dataset
        with z.open("biofile0.csv") as f:
            train = pd.read_csv(f)
            print(train.head())
            pandas_gbq.to_gbq(train, 'retrosheets.biofile0', project_id='baseball-434300')

if __name__ == "__main__":
    # fetch_people()
    # parse_zip()
    fetch_people_2()