from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.api_method import list_all


async def start(update, context):
    USERNAME = 0
    END = -1
    if not context.user_data.__contains__('logged_in'):
        keyboard_lan = [
            [InlineKeyboardButton("注 册", url='https://www.instapaper.com/'),
             InlineKeyboardButton("登 录", callback_data='login_confirm')]
        ]
        markup = InlineKeyboardMarkup(keyboard_lan)
        await update.message.reply_text(
            '欢迎使用 Instasaver！\n开始使用前，请先登录您的账号。',
            reply_markup=markup
        )
        return USERNAME
    else:
        await update.message.reply_text(
            '您已登录，可以直接使用！'
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
        await update.message.reply_text(
            '确认解绑账号吗？',
            reply_markup=markup
        )
        return CONFIRM_QUIT
    else:
        await update.message.reply_text("你还没有登录～\n前往：/start")
        return END


async def about(update, context):
    keyboard = [[InlineKeyboardButton("源 代 码", url='https://github.com/dahawong/instasaver'),
                InlineKeyboardButton("工 作 室", url='https://office.daha.me/')]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_markdown('*Instasaver*  `2.1.0`\n保存消息中的链接到你的 Instapaper。', reply_markup=markup)


async def list_command(update, context):
    await update.message.reply_text('点击获取未读列表', reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton('📃', switch_inline_query_current_chat='')))
