'''
Callback handler functions of Message updates.
'''
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ConversationHandler
from helper import INSTANT_VIEW_SUPPORTED_DOMAINS
from urllib import request
import utils.instapaper as instapaper
from utils.bookmark_preview import create_page
from utils.database import db, User

VERIFY = 2


async def reply_normal_text(update, context):
    if context.user_data.__contains__('logged_in'):
        await update.effective_message.reply_text('请发送带链接的消息，看看能不能保存到 Instapaper。')
    else:
        await update.effective_message.reply_text('请先登录 Instapaper。\n点击开始：/start')


async def request_password(update, context):
    message = update.message
    context.user_data['username'] = message.text
    msg = await message.reply_text('请输入密码：')
    context.user_data['msg_request_pwd'] = msg.message_id
    return VERIFY


async def verify_login(update, context):
    USERNAME = 0
    message = update.message
    # Get the password from the user
    password = message.text
    username = context.user_data['username']
    await update.message.delete()  # Delete password message
    await context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=context.user_data.get('msg_request_pwd')
    )
    replied_message = await message.reply_text('登录中，请稍候…')
    client = instapaper.get_client(username, password)
    if client:
        context.user_data['client'] = client
        context.user_data['logged_in'] = True
        await replied_message.edit_text(
            text=(
                '登录成功！试着发送带链接的消息，看看能不能保存到 Instapaper。\n\n'
                '另外，欢迎关注 @instasaverlog，以及时了解 bot 的运行状况。'
            )
        )

        return ConversationHandler.END
    else:
        await replied_message.edit_text(
            text='抱歉，登录失败！',
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton("重新尝试", callback_data='login_confirm'))
        )
        context.user_data.pop('username')
        return USERNAME


async def save_link(update, context):
    is_logged_in = context.user_data.__contains__('logged_in')
    message = update.effective_message
    if is_logged_in:
        client = context.user_data['client']
        # Detect if the link is from media caption or a text message
        if message.caption:
            links = list(
                message.parse_caption_entities('url').values())
            text_link_entities = filter(
                lambda x: x.type == 'text_link', message.caption_entities)
        else:
            links = list(
                message.parse_entities('url').values())
            text_link_entities = filter(
                lambda x: x.type == 'text_link', message.entities)
        text_links = list(map(
            lambda x: x if x.type == 'url' else x.url,
            text_link_entities
        ))
        links.extend(text_links)
        bookmarks = {}
        count = 0
        failed = 0
        replied_message = await message.reply_text(f"保存中 …")

        # Start saving the bookmarks
        for link in links:
            try:
                link = request.urlopen(link).geturl()
            except:
                pass
            bookmark_id, title = instapaper.save(client, link)
            html_text = instapaper.get_text(client, bookmark_id)

            # Match the domain in url
            pattern = r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)"
            match = re.match(pattern, link)
            domain = match.group(1) if match else None
            if domain and (domain in INSTANT_VIEW_SUPPORTED_DOMAINS):
                preview_url = link
            else:
                preview_url = await create_page(title or link, html_text)

            if bookmark_id:
                count += 1
                bookmarks[bookmark_id] = {
                    'title': title,
                    'link': link,
                    'preview_url': preview_url
                }
                context.user_data[str(bookmark_id)] = {
                    'preview_url': preview_url}
                await replied_message.edit_text(f"已保存（{count}/{len(links)}）…")
            else:
                failed += 1
        if count:
            failed_saving = f"另有 {failed} 篇未能保存。" if failed else ""
            await replied_message.edit_text(f"成功保存 {count} 篇文章!\n" + failed_saving)
        else:
            await message.reply_text("保存失败，请重新尝试 :(")

        # Return the saved bookmarks as messages to preview
        for bookmark_id, bookmark in bookmarks.items():
            title = bookmark['title']
            link = bookmark['link']
            preview_url = bookmark['preview_url']
            keyboard = [[
                InlineKeyboardButton(
                    "🗑", callback_data=f'delete_{bookmark_id}'),
                InlineKeyboardButton(
                    "💙", callback_data=f'like_{bookmark_id}')
            ], [InlineKeyboardButton("移动到…", switch_inline_query_current_chat=f'move_{bookmark_id}_to'), InlineKeyboardButton("查看文章列表", switch_inline_query_current_chat='#')]]
            if title:
                message_text = (
                    f"<a href='{preview_url or link}'><strong>{title}</strong></a>\n"
                    f"<a href='{link}'>原文</a> | <a href='https://www.instapaper.com/read/{bookmark_id}'>Instapaper</a>"
                )
            else:
                message_text = (
                    f"<strong>{preview_url or link}</strong>\n"
                    f"<a href='{link}'>原文</a> | <a href='https://www.instapaper.com/read/{bookmark_id}'>Instapaper</a>"
                )
            markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=message_text,
                reply_markup=markup,
                parse_mode=ParseMode.HTML
            )
    else:
        await update.effective_message.reply_text('请先登录 Instapaper。\n点击开始：/start')


async def move_bookmark(update, context):
    client = context.user_data['client']
    text = update.effective_message.text
    match = re.match(r"^move_(\d+)_to_(\d+)$", text)
    bookmark_id, folder_id = match.group(1), match.group(2)
    title = instapaper.move(client, bookmark_id, folder_id)
    if (title):
        await update.effective_message.reply_text(f"《{title}》移动成功~")
        await update.effective_message.delete()
    else:
        await update.effective_message.reply_text("移动失败 :(")


async def delete_message(update, context):
    await update.effective_message.delete()
