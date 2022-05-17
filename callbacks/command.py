from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import meta


async def start(update, context):
    USERNAME = 0
    END = -1
    # Initialize user_data
    context.user_data['message_to_delete'] = []
    if not context.user_data.__contains__('logged_in'):
        keyboard_lan = [
            [InlineKeyboardButton("注 册", url='https://www.instapaper.com/'),
             InlineKeyboardButton("登 录", callback_data='login_confirm')]
        ]
        markup = InlineKeyboardMarkup(keyboard_lan)
        await update.effective_message.reply_text(
            '欢迎使用 Instasaver！\n开始使用前，请先登录您的账号。',
            reply_markup=markup
        )
        return USERNAME
    else:
        await update.effective_message.reply_text(
            text='您已登录，可以直接使用！',
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton('查看文章列表', switch_inline_query_current_chat=''))
        )
        return END


async def quit_(update, context):
    CONFIRM_QUIT = 0
    END = -1
    if context.user_data.__contains__('logged_in'):
        keyboard = [
            [InlineKeyboardButton("返 回", callback_data='cancel_quit'),
             InlineKeyboardButton("解 绑", callback_data='confirm_quit')
             ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.effective_message.reply_text(
            '确认解绑账号吗？',
            reply_markup=markup
        )
        return CONFIRM_QUIT
    else:
        await update.effective_message.reply_text("你还没有登录～\n前往：/start")
        return END


async def about(update, context):
    keyboard = [[InlineKeyboardButton("源 代 码", url='https://github.com/DahaWong/instasaver'),
                InlineKeyboardButton("工 作 室", url='https://dreamlong.design/')]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_markdown(
        (f"*Instasaver*  `{meta['version']}`\n"
         "保存消息中的链接到你的 Instapaper。\n\n"
         "由 @dahawong 制作"
         ), reply_markup=markup)
