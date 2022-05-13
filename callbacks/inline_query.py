from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from utils.api_method import list_all


async def get_all_unread(update, context):
    client = context.user_data.get('client')

    def format_unread(bookmark):
        bookmark_id = bookmark['bookmark_id']
        keyboard = [[
            InlineKeyboardButton("🗑", callback_data=f'delete_{bookmark_id}'),
            InlineKeyboardButton("💙", callback_data=f'like_{bookmark_id}')
        ]]
        return InlineQueryResultArticle(
            id=bookmark['bookmark_id'],
            title=bookmark['title'] or bookmark['url'],
            input_message_content=InputTextMessageContent(bookmark['url']),
            description=bookmark['description'] or bookmark['url'],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    await update.inline_query.answer(
        list(map(format_unread, list_all(client))),
        auto_pagination=True,
    )
