'''
Callback handler functions of InlineQuery updates.
'''

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from utils import instapaper
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
        keyboard = [[InlineKeyboardButton(
            "查看文章列表", switch_inline_query_current_chat='#'), InlineKeyboardButton("移动到…", switch_inline_query_current_chat=f'move_{bookmark_id}_to')]]
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
        [format_unread(x, context) for x in instapaper.list_all(client)],
        auto_pagination=True,
        cache_time=0
    )


async def get_folders(update, context):
    client = context.user_data.get('client')
    folders = instapaper.get_folders(client)
    
    await update.inline_query.answer(
        [InlineQueryResultArticle(
            id=folder.get('folder_id'),
            title=folder.get('display_title') or folder.get('title'),
            input_message_content=InputTextMessageContent(
                message_text="📁 " + folder.get('title'))
        ) for folder in folders],
        auto_pagination=True
    )


async def select_folder_to_move(update, context):
    query = update.inline_query.query
    client = context.user_data.get('client')
    folders = instapaper.get_folders(client)
    
    if folders:
        results = [InlineQueryResultArticle(
            id=folder.get('folder_id'),
            title=folder.get('display_title') or folder.get('title'),
            input_message_content=InputTextMessageContent(
                message_text="_".join(
                    [query, str(folder.get('folder_id'))])
            )
        ) for folder in folders]
    else:
        results = [InlineQueryResultArticle(
            id=0,
            title="还没有创建文件夹",
            input_message_content=InputTextMessageContent(
                message_text="前往 <a href='https://www.instapaper.com'>Instapaper</a> 创建文件夹",
                parse_mode=ParseMode.HTML
            )
        )]
        
    await update.inline_query.answer(
        results,
        auto_pagination=True,
        cache_time=600
    )