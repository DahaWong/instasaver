from telegram.ext import InlineQueryHandler
import callbacks.inline_query as callbacks

all_unread_handler = InlineQueryHandler(
    callbacks.get_all_unread, pattern=r'^\#$')

select_folder_handler = InlineQueryHandler(
    callbacks.select_folder_to_move, pattern=r'^move_(?:\d+)_to$')
