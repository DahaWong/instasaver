from telegram.ext import CallbackQueryHandler
import callbacks.callback_query as callback

login_confirm_handler = CallbackQueryHandler(
    callback.request_username, pattern='^login_confirm$')

request_delete_link_handler = CallbackQueryHandler(
    callback.request_delete_link, pattern='^delete_')

confirm_delete_link_handler = CallbackQueryHandler(
    callback.confirm_delete_link, pattern='^delete_')

cancel_delete_link_handler = CallbackQueryHandler(
    callback.cancel_delete_link, pattern='^cancel_delete$')

like_link_handler = CallbackQueryHandler(callback.like_link, pattern='^like_')

unlike_link_handler = CallbackQueryHandler(
    callback.unlike_link, pattern='^unlike_')

# archive_link_handler = CallbackQueryHandler(callback.archive_link, pattern='^archive_')

# unarchive_link_handler = CallbackQueryHandler(
#     callback.unarchive_link, pattern='^unarchive_')


quit_cancel_handler = CallbackQueryHandler(
    callback.cancel_quit, pattern='^cancel_quit$')

quit_confirm_handler = CallbackQueryHandler(
    callback.confirm_quit, pattern='^confirm_quit$')
