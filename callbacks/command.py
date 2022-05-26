'''
Callback handler functions of Command updates.
'''

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from config import meta
from constants import BOT_NAME, DEVELOPER_TELEGRAM_USERNAME, REPOSITORY_URL, STUDIO_URL, WHITE_SQUARE
from utils import instapaper


async def start(update, context):
    USERNAME = 0
    # Initialize user_data
    context.user_data['message_to_delete'] = []
    if not context.user_data.__contains__('logged_in'):
        keyboard_lan = [
            [InlineKeyboardButton("注 册", url='https://www.instapaper.com/'),
             InlineKeyboardButton("登 录", callback_data='login_confirm')]
        ]
        markup = InlineKeyboardMarkup(keyboard_lan)
        await update.effective_message.reply_text(
            f'欢迎使用 {BOT_NAME}！\n开始使用前，请先登录您的账号。',
            reply_markup=markup
        )
        return USERNAME
    else:
        await update.effective_message.reply_text(
            text='您已登录，可以直接使用！',
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton('查看文章列表', switch_inline_query_current_chat='#'))
        )
        return ConversationHandler.END


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
            '确认解绑账号吗？这将会清除您在本机器人中所有的数据。',
            reply_markup=markup
        )
        return CONFIRM_QUIT
    else:
        await update.effective_message.reply_text("你还没有登录～\n前往：/start")
        return END


async def about(update, context):
    keyboard = [[InlineKeyboardButton("源 代 码", url=REPOSITORY_URL),
                InlineKeyboardButton("工 作 室", url=STUDIO_URL)]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_markdown(
        (f"*{BOT_NAME}*  `{meta['version']}`\n"
         "保存消息中的链接到你的 Instapaper。\n\n"
         f"由 @{DEVELOPER_TELEGRAM_USERNAME} 制作"
         ), reply_markup=markup)


async def test(update, context):
    client = context.user_data['client']
    folders = instapaper.get_folders(client)
    print(folders)
