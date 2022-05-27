'''
Callback handler functions of CallbackQuery updates.
'''

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler, CallbackContext
from telegram.constants import ParseMode
from utils.instapaper import delete, like, unlike
import re
from utils.database import *

REQUEST_DELETE, = range(1)


async def request_username(update: Update, context:CallbackContext):
    PASSWORD = 1
    await update.effective_message.edit_text(
        text="请输入<strong>用户名</strong>或者<strong>邮箱</strong>：",
        parse_mode=ParseMode.HTML
    )
    return PASSWORD


async def request_delete_link(update: Update, context:CallbackContext):
    message = update.effective_message
    if message:
        context.user_data['message_to_delete'].append(message.message_id)
    await message.reply_text(
        text='确定要删除这个链接吗？',
        reply_markup=InlineKeyboardMarkup.from_row([
            InlineKeyboardButton(
                '确定', callback_data=update.callback_query.data),
            InlineKeyboardButton('取消', callback_data='cancel_delete')]
        )
    )
    return REQUEST_DELETE


async def confirm_delete_link(update: Update, context:CallbackContext):
    query = update.callback_query
    pattern = '(delete_)([0-9]+)'
    bookmark_id: str = re.match(pattern, query.data).group(2)
    client = context.user_data['client']
    delete(client, bookmark_id)
    for message_id in context.user_data['message_to_delete']:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=message_id
        )
    context.user_data.pop(bookmark_id)
    context.user_data['message_to_delete'].clear()
    await query.edit_message_text('删除成功～')
    return ConversationHandler.END


async def cancel_delete_link(update: Update, context:CallbackContext):
    query = update.callback_query
    await query.answer('已取消～')
    await query.delete_message()
    context.user_data['message_to_delete'].clear()
    return ConversationHandler.END


async def like_link(update: Update, context:CallbackContext):
    message = update.effective_message
    data = update.callback_query.data
    client = context.user_data['client']
    pattern = '(like_)([0-9]+)'
    bookmark_id = re.match(pattern, data).group(2)
    if like(client, bookmark_id):
        await message.pin(disable_notification=True)
        keyboard = [[
            InlineKeyboardButton("🗑", callback_data=f'delete_{bookmark_id}'),
            InlineKeyboardButton("❤️", callback_data=f'unlike_{bookmark_id}')
        ], [InlineKeyboardButton("移动到…", switch_inline_query_current_chat=f'move_{bookmark_id}_to'), InlineKeyboardButton("查看文章列表", switch_inline_query_current_chat='#')]]
        await message.edit_reply_markup(InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_text('操作失败 :(')


async def unlike_link(update: Update, context:CallbackContext):
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


async def cancel_quit(update: Update, context:CallbackContext):
    query = update.callback_query
    await query.delete_message()
    await query.answer('已返回，可以继续保存文章啦。')
    return ConversationHandler.END


async def confirm_quit(update: Update, context:CallbackContext):
    # TODO: set cascading delete rule
    username = update.effective_user.username
    (User
        .select()
        .where(User.username == username)
        .get()
        .delete_instance())
    context.user_data.clear()
    await update.callback_query.edit_message_text('解绑成功！')
    return ConversationHandler.END
