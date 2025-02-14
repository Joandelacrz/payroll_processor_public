import os

def check_auth(username, password):
    return username == os.environ.get('API_USER', 'user') and password == os.environ.get('API_PWD', 'pwd')
