import functions_framework
from markupsafe import escape

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