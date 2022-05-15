from telegram.ext import MessageHandler
from telegram.ext import filters
import callbacks.message as callback

username_handler = MessageHandler(filters.TEXT, callback.request_password)
password_handler = MessageHandler(filters.TEXT, callback.verify_login)

link_handler = MessageHandler(~filters.VIA_BOT & (filters.Entity(
    'url') | filters.Entity('text-link')), callback.save_link)
normal_text_handler = MessageHandler(~filters.VIA_BOT & filters.TEXT & ~(filters.Entity(
    'url') | filters.Entity('text-link')), callback.reply_normal_text)
