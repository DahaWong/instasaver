import config
from telegram.ext import ApplicationBuilder
from handlers.register import register
from utils.persistence import bot_persistence

application = (ApplicationBuilder()
               .token(config.bot_token)
               .persistence(bot_persistence)
               .build())

register(application)
application.run_polling()
