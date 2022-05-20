from telegram.ext import MessageHandler
from telegram.ext import filters
import callbacks.message as callback

username_handler = MessageHandler(filters.TEXT, callback.request_password)
password_handler = MessageHandler(filters.TEXT, callback.verify_login)


link_handler = MessageHandler(
    ~filters.VIA_BOT &
    (filters.Entity('url') |
     filters.Entity('text_link') |
     filters.CaptionEntity('text_link') |
     filters.CaptionEntity('url')
     ), callback.save_link)


normal_text_handler = MessageHandler(
    ~filters.VIA_BOT &
    ~filters.COMMAND &
    ~filters.Entity('text_link') &
    ~filters.CaptionEntity('text_link') &
    ~filters.CaptionEntity('url'), callback.reply_normal_text)


move_bookmark_handler = MessageHandler(
    filters.TEXT &
    filters.VIA_BOT, callback.move_bookmark)
