import functions_framework
from urllib.request import urlopen
from google.cloud import storage

BASE_URL = 'https://www.retrosheet.org'
PROJECT_ID = 'baseball-434918'
BUCKET_NAME = 'retrosheets'


def write_to_gcs(data, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    with blob.open("wb") as f:
        f.write(data)


@functions_framework.http
def fetch_file(request):
    content_type = request.headers["content-type"]
    if content_type == "application/json":
        request_json = request.get_json(silent=True)
        if request_json and "file_path" in request_json:
            file_path = request_json["file_path"]
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    else:
        raise ValueError(f"Content type requires 'application/json' but given '{content_type}'")
    resp = urlopen(f'{BASE_URL}/{file_path}')
    write_to_gcs(resp.read(), file_path)
