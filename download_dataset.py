import requests
import os

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":

    test_id = '1fZzD1Jm04TpJJiv40ebRvk4ZO3cOGEX1'
    destination = 'data/test.tar.gz'
    if not os.path.exists(destination):
        download_file_from_google_drive(test_id, destination)

    train_id = '1BLlAVl6FgEO3qsOXaJXILcnL3Twyhbj6'
    destination = 'data/train.tar.gz'
    if not os.path.exists(destination):
        download_file_from_google_drive(train_id, destination)

    valid_id = '1EIMM8seDhgVv5InldDZKsaiShaBo0uZh'
    destination = 'data/valid.tar.gz'
    if not os.path.exists(destination):
        download_file_from_google_drive(valid_id, destination)
