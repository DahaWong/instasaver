from telegram.ext import CommandHandler
import callbacks.command as callback
from telegram.ext import filters
from config import dev_user_id

start_handler = CommandHandler('start', callback.start)
about_handler = CommandHandler('about', callback.about)
quit_handler = CommandHandler('quit', callback.quit_)
# setting_handler = CommandHandler('setting', callback.setting)

# Dev Commands
get_users_handler = CommandHandler('users', callback.get_users, filters=filters.Chat(dev_user_id))
get_chat_id_handler = CommandHandler('get_chat_id', callback.get_chat_id, filters=filters.Chat(dev_user_id))
init_commands_handler = CommandHandler('init_commands', callback.init_commands, filters=filters.Chat(dev_user_id))