from telegram.ext import InlineQueryHandler
import callbacks.inline_query as callbacks

all_unread_handler = InlineQueryHandler(callbacks.get_all_unread)
