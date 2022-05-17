import configparser
from utils.persistence import bot_persistence

config = configparser.ConfigParser()
config.read('config.ini')


# Bot
bot_token_test = config['BOT']['TOKEN_TEST']
bot_token = config['BOT']['TOKEN']
proxy = config['BOT']['PROXY']


# Oauth
oauth_consumer_id = config['OAUTH']['CONSUMER_ID']
oauth_consumer_secret = config['OAUTH']['CONSUMER_SECRET']

# Meta
meta = {
    'version': '2.2.0'
}
