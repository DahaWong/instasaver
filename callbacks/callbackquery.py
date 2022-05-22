'''
Callback handler functions of CallbackQuery updates.
'''

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram.constants import ParseMode
from utils.instapaper import delete, like, unlike
from utils.persistence import bot_persistence
import re

REQUEST_DELETE, = range(1)


async def request_username(update, context):
    PASSWORD = 1
    bot = context.bot
    query = update.callback_query
    await bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="请输入<strong>用户名</strong>或者<strong>邮箱</strong>：",
        parse_mode=ParseMode.HTML
    )
    return PASSWORD


async def request_delete_link(update, context):
    if update.callback_query.message:
        context.user_data['message_to_delete'].append(
            update.callback_query.message.message_id)
    await update.effective_message.reply_text(
        text='确定要删除这个链接吗？',
        reply_markup=InlineKeyboardMarkup.from_row([
            InlineKeyboardButton(
                '确定', callback_data=update.callback_query.data),
            InlineKeyboardButton('取消', callback_data='cancel_delete')]
        )
    )
    await bot_persistence.flush()
    return REQUEST_DELETE


async def confirm_delete_link(update, context):
    query = update.callback_query
    pattern = '(delete_)([0-9]+)'
    bookmark_id: str = re.match(pattern, query.data).group(2)
    client = context.user_data['client']
    delete(client, bookmark_id)
    await query.edit_message_text('删除成功～')
    for message_id in context.user_data['message_to_delete']:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=message_id
        )
    context.user_data.pop(bookmark_id)
    context.user_data['message_to_delete'].clear()
    await bot_persistence.flush()
    return ConversationHandler.END


async def cancel_delete_link(update, context):
    await update.callback_query.answer('已取消～')
    await update.callback_query.delete_message()
    context.user_data['message_to_delete'].clear()
    await bot_persistence.flush()
    return ConversationHandler.END


async def like_link(update, context):
    message = update.effective_message
    data = update.callback_query.data
    client = context.user_data['client']
    pattern = '(like_)([0-9]+)'
    bookmark_id = re.match(pattern, data).group(2)
    if like(client, bookmark_id):
        message = update.callback_query.message
        await message.pin(disable_notification=True)
        keyboard = [[
            InlineKeyboardButton("🗑", callback_data=f'delete_{bookmark_id}'),
            InlineKeyboardButton("❤️", callback_data=f'unlike_{bookmark_id}')
        ], [InlineKeyboardButton("移动到…", switch_inline_query_current_chat=f'move_{bookmark_id}_to'), InlineKeyboardButton("查看文章列表", switch_inline_query_current_chat='#')]]
        await message.edit_reply_markup(InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_text('操作失败 :(')


async def unlike_link(update, context):
    message = update.effective_message
    data = update.callback_query.data
    client = context.user_data['client']
    pattern = r'(unlike_)([0-9]+)'
    bookmark_id = re.match(pattern, data).group(2)
    if unlike(client, bookmark_id):
        await message.unpin()
        keyboard = [[
            InlineKeyboardButton("🗑", callback_data=f'delete_{bookmark_id}'),
            InlineKeyboardButton("💙", callback_data=f'like_{bookmark_id}')
        ], [InlineKeyboardButton("移动到…", switch_inline_query_current_chat=f'move_{bookmark_id}_to'), InlineKeyboardButton("查看文章列表", switch_inline_query_current_chat='#')]]
        await message.edit_reply_markup(InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_text('操作失败 :(')


async def cancel_quit(update, context):
    query = update.callback_query
    await query.delete_message()
    await query.answer('已返回，可以继续保存文章啦。')
    return ConversationHandler.END


async def confirm_quit(update, context):
    context.user_data.clear()
    await bot_persistence.flush()
    await update.callback_query.edit_message_text('解绑成功！')
    return ConversationHandler.END
