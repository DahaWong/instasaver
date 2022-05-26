from telegram.ext import ConversationHandler
from handlers.command import start_handler, quit_handler
from handlers.callback_query import login_confirm_handler, quit_cancel_handler, quit_confirm_handler, request_delete_link_handler, confirm_delete_link_handler, cancel_delete_link_handler
from handlers.message import password_handler, username_handler

USERNAME, PASSWORD, VERIFY = range(3)
CONFIRM_QUIT, = range(1)
REQUEST_DELETE, = range(1)

login_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        USERNAME: [login_confirm_handler],
        PASSWORD: [username_handler],
        VERIFY: [password_handler]
    },
    fallbacks=[start_handler],
    allow_reentry=True
)

quit_handler = ConversationHandler(
    entry_points=[quit_handler],
    states={
        CONFIRM_QUIT: [quit_cancel_handler, quit_confirm_handler]
    },
    fallbacks=[quit_handler],
    allow_reentry=True
)

delete_link_handler = ConversationHandler(
    entry_points=[request_delete_link_handler],
    states={
        REQUEST_DELETE: [confirm_delete_link_handler,
                         cancel_delete_link_handler]
    },
    fallbacks=[cancel_delete_link_handler],
    allow_reentry=False
)