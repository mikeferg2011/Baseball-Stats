import os
from google.cloud import bigquery
from google.cloud import storage

# to authenticate as service account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{os.getcwd()}/sa_key.json'

def create_bq_dataset(data_name: str):
    client = bigquery.Client()
    dataset_id = f"{client.project}.{data_name}"
    dataset = bigquery.Dataset(dataset_id)
    # TODO(developer): Specify the geographic location where the dataset should reside.
    dataset.location = "US"
    dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
    print(f"Created dataset {client.project}.{dataset.dataset_id}")

def create_gcs_bucket(bucket_name: str):
    """Creates a new bucket"""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name, location='us-central1')
    print(f"Bucket {bucket.name} created")

if __name__ == '__main__':
    create_bq_dataset('retrosheets')
    create_gcs_bucket('retrosheets')