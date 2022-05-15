from handlers import conversation
from handlers.message import link_handler, normal_text_handler
from handlers.callbackquery import unlike_link_handler, like_link_handler
from handlers.command import about_handler, list_handler
from handlers.inline_query import all_unread_handler

handlers = [conversation.login_handler,
            conversation.quit_handler,
            conversation.delete_link_handler, 
            about_handler, list_handler, all_unread_handler]
handlers.extend([link_handler, normal_text_handler])
handlers.extend([unlike_link_handler, like_link_handler])


def register(application):
    for handler in handlers:
        application.add_handler(handler)
