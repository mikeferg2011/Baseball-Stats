import functions_framework
import parse_helper as ph


# @functions_framework.http
# def hello_content(request):
#     """Responds to an HTTP request using data from the request body parsed
#     according to the "content-type" header.
#     Args:
#         request (flask.Request): The request object.
#         <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
#     Returns:
#         The response text, or any set of values that can be turned into a
#         Response object using `make_response`
#         <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
#     """
#     content_type = request.headers["content-type"]
#     if content_type == "application/json":
#         request_json = request.get_json(silent=True)
#         if request_json and "name" in request_json:
#             name = request_json["name"]
#         else:
#             raise ValueError("JSON is invalid, or missing a 'name' property")
#     elif content_type == "application/octet-stream":
#         name = request.data
#     elif content_type == "text/plain":
#         name = request.data
#     elif content_type == "application/x-www-form-urlencoded":
#         name = request.form.get("name")
#     else:
#         raise ValueError(f"Unknown content type: {content_type}")
#     return f"Hello {escape(name)}!"

FILE_DICT = {
    'ballparks': ph.BallparkParser,
    'teams': ph.TeamsParser,
    'bios': ph.PeopleParser,
}


@functions_framework.http
def process_zip(request):
    content_type = request.headers['content-type']
    assert content_type == 'application/json', f'Content type requires "application/json" but given "{content_type}"'

    request_json = request.get_json()
    file_path = request_json['file_path']
    data_type = request_json['data_type']
    # TODO make write mode optional in pipeline call
    write_mode = request_json.get('write_mode')
    
    # add if on data_type 
    FILE_DICT[data_type](file_path).pipeline()
    return f'{file_path} loaded successfully'
