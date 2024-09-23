import functions_framework
import parse_helper as ph


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
