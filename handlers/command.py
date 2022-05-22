from telegram.ext import CommandHandler
import callbacks.command as callback

start_handler = CommandHandler('start', callback.start)
about_handler = CommandHandler('about', callback.about)
quit_handler = CommandHandler('quit', callback.quit_)
# setting_handler = CommandHandler('setting', callback.setting)
test_handler = CommandHandler('test', callback.test)
