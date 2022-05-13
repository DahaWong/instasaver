from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import re
from utils.api_method import delete, like, unlike
from utils.persistence import bot_persistence


async def request_username(update, context):
    PASSWORD = 1
    bot = context.bot
    query = update.callback_query
    await bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="请输入<strong>用户名</strong>或者<strong>邮箱</strong>：",
        parse_mode='HTML'
    )
    return PASSWORD


async def delete_link(update, context):
    bot = context.bot
    message = update.callback_query.message
    data = update.callback_query.data
    client = context.user_data['client']
    pattern = '(delete_)([0-9]+)'
    bookmark_id = re.match(pattern, data).group(2)
    delete(client, bookmark_id)
    await bot_persistence.flush()
    await message.delete()
    await bot.answer_callback_query(
        update.callback_query.id,
        '已删除～'
    )


async def like_link(update, context):
    bot = context.bot
    data = update.callback_query.data
    client = context.user_data['client']
    pattern = '(like_)([0-9]+)'
    bookmark_id = re.match(pattern, data).group(2)
    if like(client, bookmark_id):
        keyboard = [[
            InlineKeyboardButton("🗑", callback_data=f'delete_{bookmark_id}'),
            InlineKeyboardButton("❤️", callback_data=f'unlike_{bookmark_id}')
        ]]
        message = update.callback_query.message
        markup = InlineKeyboardMarkup(keyboard)
        await bot.edit_message_reply_markup(
            chat_id=message.chat_id,
            message_id=message.message_id,
            reply_markup=markup
        )
    else:
        await bot.answer_callback_query(
            update.callback_query.id,
            ':('
        )


async def unlike_link(update, context):
    bot = context.bot
    data = update.callback_query.data
    client = context.user_data['client']
    pattern = r'(unlike_)([0-9]+)'
    bookmark_id = re.match(pattern, data).group(2)
    if unlike(client, bookmark_id):
        keyboard = [[
            InlineKeyboardButton("🗑", callback_data=f'delete_{bookmark_id}'),
            InlineKeyboardButton("💙", callback_data=f'like_{bookmark_id}')
        ]]
        message = update.callback_query.message
        markup = InlineKeyboardMarkup(keyboard)
        await bot.edit_message_reply_markup(
            chat_id=message.chat_id,
            message_id=message.message_id,
            reply_markup=markup
        )
    else:
        await bot.answer_callback_query(
            update.callback_query.id,
            ':('
        )


async def cancel_quit(update, context):
    END = -1
    query = update.callback_query
    await context.bot.delete_message(
        query.message.chat_id,
        query.message.message_id
    )
    await context.bot.answer_callback_query(
        query.id,
        '已返回，可以继续保存文章啦。'
    )
    return END


async def confirm_quit(update, context):
    END = -1
    context.user_data.clear()
    await bot_persistence.flush()
    bot = context.bot
    query = update.callback_query
    await bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='解绑成功！'
    )
    return END
