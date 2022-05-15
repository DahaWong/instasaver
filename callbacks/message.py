from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from utils.persistence import bot_persistence
from utils.api_method import get_client, save

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
        await bot_persistence.flush()
        await bot.edit_message_text(
            chat_id=message.chat_id,
            message_id=message.message_id,
            text='登录成功！试着发送带链接的消息，看看能不能保存到 Instapaper。\n\n另外，欢迎关注 @instasaverlog，以及时了解 bot 的运行状况。'
        )
        context.user_data['logged_in'] = True
        await bot_persistence.flush()
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
        links = list(update.message.parse_entities('url').values())
        text_link_entities = filter(
            lambda x: x.type == 'text_link', update.message.entities)
        text_links = list(map(lambda x: x if x.type ==
                          'url' else x.url, text_link_entities))
        links.extend(text_links)
        link_ids = {}
        titles = {}
        count = 0
        failed = 0
        message_saving = await update.message.reply_text(f"保存中 …")

        # Start saving
        for link in links:
            bookmark_id, title = save(client, link)
            link_ids[link] = bookmark_id
            titles[bookmark_id] = title
            if bookmark_id:
                count += 1
                await message_saving.edit_text(f"已保存（{count}/{len(links)}）…")
            else:
                failed += 1
            await bot_persistence.flush()

        if count:
            failed_saving = f"另有 {failed} 篇未能保存。" if failed else ""
            await message_saving.edit_text(f"成功保存 {count} 篇文章!\n" + failed_saving)
        else:
            await update.message.reply_text("保存失败，请重新尝试 :(")

        # Return the saved articles as preview messages
        for link in links:
            bookmark_id = link_ids[link]
            title = titles[bookmark_id]
            keyboard = [[
                InlineKeyboardButton(
                    "🗑", callback_data=f'delete_{bookmark_id}'),
                InlineKeyboardButton(
                    "💙", callback_data=f'like_{bookmark_id}')
            ], [InlineKeyboardButton("查看文章列表", switch_inline_query_current_chat='')]]
            markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"<a href='https://www.instapaper.com/read/{bookmark_id}'>{title}</a>" if title else link,
                reply_markup=markup,
                parse_mode=ParseMode.HTML
            )
    else:
        await update.message.reply_text('请先登录 Instapaper。\n点击开始：/start')
