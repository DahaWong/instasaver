from telegram.ext import CommandHandler
import callbacks.command as callback

start_handler = CommandHandler('start', callback.start)
about_handler = CommandHandler('about', callback.about)
quit_handler = CommandHandler('quit', callback.quit_)
test_handler = CommandHandler('test', callback.test)
