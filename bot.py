import config
from telegram.ext import ApplicationBuilder
from handlers.register import register
from utils.persistence import bot_persistence

# objects = []
# with (open("persistence", "rb")) as openfile:
#     while True:
#         try:
#             objects.append(pickle.load(openfile))
#         except EOFError:
#             break

application = ApplicationBuilder().token(
    config.bot_token).persistence(bot_persistence).build()

register(application)

application.run_polling()
