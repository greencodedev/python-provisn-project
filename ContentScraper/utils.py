

def get_fear_and_greed_data():
    from requests import Session
    from json import loads
    get_url = 'https://api.alternative.me/fng/'
    session = Session()
    response = session.get(get_url)
    data = loads(response.text)
    return data
