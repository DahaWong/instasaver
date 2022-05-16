from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from utils.persistence import bot_persistence
from utils.instapaper import get_client, get_text, save
from utils.bookmark_preview import create_page

VERIFY = 2


async def reply_normal_text(update, context):
    if context.user_data.__contains__('logged_in'):
        await update.message.reply_text('请发送带链接的消息，看看能不能保存到 Instapaper。')
    else:
        await update.message.reply_text('请先登录 Instapaper。\n点击开始：/start')


async def request_password(update, context):
    # 记录使用者的 Instapaper 登录名（username）
    context.user_data['username'] = update.message.text
    await update.message.reply_text('请输入密码：')
    return VERIFY


async def verify_login(update, context):
    END = -1
    USERNAME = 0
    bot = context.bot
    # 记录使用者的 Instapaper 密码（password）
    context.user_data['password'] = update.message.text
    await update.message.delete()
    message = await update.message.reply_text('登录中，请稍候…')
    if get_client(context.user_data):
        context.user_data['client'] = get_client(context.user_data)
        context.user_data['logged_in'] = True
        context.user_data.pop('password') # Remove password upon logged in.
        await bot_persistence.flush()
        await bot.edit_message_text(
            chat_id=message.chat_id,
            message_id=message.message_id,
            text='登录成功！试着发送带链接的消息，看看能不能保存到 Instapaper。\n\n另外，欢迎关注 @instasaverlog，以及时了解 bot 的运行状况。'
        )
        return END
    else:
        keyboard = [[InlineKeyboardButton(
            "重新尝试", callback_data='login_confirm')]]
        markup = InlineKeyboardMarkup(keyboard)
        await bot.edit_message_text(
            chat_id=message.chat_id,
            message_id=message.message_id,
            text='抱歉，登录失败！',
            reply_markup=markup
        )
        context.user_data.pop('username')
        context.user_data.pop('password')
        return USERNAME


async def save_link(update, context):
    logged_in = context.user_data.__contains__('client')
    if logged_in:
        client = context.user_data['client']
        if not update.message.caption:
            links = list(update.message.parse_entities('url').values())
            text_link_entities = filter(
                lambda x: x.type == 'text_link', update.message.entities)
        else:
            links = list(update.message.parse_caption_entities('url').values())
            text_link_entities = filter(
                lambda x: x.type == 'text_link', update.message.caption_entities)
        text_links = list(map(lambda x: x if x.type ==
                          'url' else x.url, text_link_entities))
        links.extend(text_links)
        bookmarks = {}
        count = 0
        failed = 0
        message_saving = await update.message.reply_text(f"保存中 …")

        # Start saving
        for link in links:
            bookmark_id, title = save(client, link)
            html_text = get_text(client, bookmark_id)
            preview_url = await create_page(title or link, html_text)
            if bookmark_id:
                count += 1
                bookmarks[bookmark_id] = {
                    'title': title,
                    'link': link,
                    'preview_url': preview_url
                }
                context.user_data[str(bookmark_id)] = {'preview_url':preview_url}
                await message_saving.edit_text(f"已保存（{count}/{len(links)}）…")
            else:
                failed += 1
            await bot_persistence.flush()
        if count:
            failed_saving = f"另有 {failed} 篇未能保存。" if failed else ""
            await message_saving.edit_text(f"成功保存 {count} 篇文章!\n" + failed_saving)
        else:
            await update.message.reply_text("保存失败，请重新尝试 :(")

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
            ], [InlineKeyboardButton("查看文章列表", switch_inline_query_current_chat='')]]
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
                chat_id=update.message.chat_id,
                text=message_text,
                reply_markup=markup,
                parse_mode=ParseMode.HTML
            )
    else:
        await update.message.reply_text('请先登录 Instapaper。\n点击开始：/start')
