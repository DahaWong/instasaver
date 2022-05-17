import configparser

config = configparser.ConfigParser()
config.read('config.ini')


# Bot
bot_token = config['BOT']['TOKEN']

# Instapaper Oauth Info
oauth_consumer_id = config['OAUTH']['CONSUMER_ID']
oauth_consumer_secret = config['OAUTH']['CONSUMER_SECRET']

# Meta
meta = {
    'version': '2.2.0'
}
