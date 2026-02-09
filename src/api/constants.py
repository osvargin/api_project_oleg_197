import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
TEST_USERNAME = os.getenv('TEST_USERNAME')
TEST_TOKEN = os.getenv('TEST_TOKEN')

AUTHORIZE_PATH = '/authorize'
MEME_PATH = '/meme'

CONTENT_TYPE_JSON = 'application/json'
AUTHORIZATION_HEADER = 'Authorization'

INVALID_AUTH_TOKEN = 'wrong_token_123456789'

NOT_EXISTING_MEME_ID = 99999999999999999999999999999999999