from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from utils.instapaper import list_all
from telegram.constants import ParseMode
from math import floor


async def get_all_unread(update, context):
    client = context.user_data.get('client')

    def format_unread(bookmark, context):
        bookmark_id = bookmark['bookmark_id']
        title = bookmark['title']
        link = bookmark['url']
        # Check if user_data has the preview url, which means the bookmark had been saved to our bot before
        preview_url = context.user_data.get(str(bookmark_id)).get(
            'preview_url') if context.user_data.get(str(bookmark_id)) else None
        progress_count = floor(bookmark['progress'] * 5)
        # keyboard = [[
        #     InlineKeyboardButton("🗑", callback_data=f'delete_{bookmark_id}'),
        #     InlineKeyboardButton("💙", callback_data=f'like_{bookmark_id}')
        # ],[InlineKeyboardButton("查看文章列表", switch_inline_query_current_chat='')]]
        keyboard = [[[InlineKeyboardButton("查看文章列表", switch_inline_query_current_chat='')]]]
        return InlineQueryResultArticle(
            id=bookmark_id,
            title=title or link,
            input_message_content=InputTextMessageContent(
                message_text=(
                    f"<a href='{preview_url or link}'><strong>{title or preview_url or link}</strong></a>\n"
                    f"<a href='{link}'>原文</a> | <a href='https://www.instapaper.com/{bookmark_id}'>Instapaper</a>"
                ),
                parse_mode=ParseMode.HTML
            ),
            url=bookmark['url'],
            description=''.join(
                ['■'*progress_count,
                 '□'*(5-progress_count),
                 f" {round(bookmark['progress']*100)}%",
                 ]),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    await update.inline_query.answer(
        [format_unread(x, context) for x in list_all(client)],
        auto_pagination=True,
        cache_time=120
    )
