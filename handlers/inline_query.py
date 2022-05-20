from telegram.ext import InlineQueryHandler
import callbacks.inline_query as callbacks

get_folders_handler = InlineQueryHandler(
    callbacks.get_folders, pattern=r'^\/$')

all_unread_handler = InlineQueryHandler(
    callbacks.get_all_unread, pattern=r'^\#$')

select_folder_handler = InlineQueryHandler(
    callbacks.select_folder_to_move, pattern=r'^move_(?:\d+)_to$')
