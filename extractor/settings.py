import os
from dotenv import load_dotenv

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# load env
dotenv_path = os.path.join(BASE_PATH, '.env')
load_dotenv(dotenv_path)

# Quebec 511
qc511_base_url = os.environ.get('QC511_BASE_URL')
qc511_road_list = os.environ.get('QC511_ROAD_LIST')

# Twitter
twitter_api_key = os.environ.get('TWITTER_API_KEY')
twitter_api_secret_key = os.environ.get('TWITTER_API_SECRET_KEY')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
