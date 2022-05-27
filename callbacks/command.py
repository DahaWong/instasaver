"""
Callback handler functions of Command updates.
"""

from telegram import BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats, BotCommandScopeChat, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler, CallbackContext
from config import meta, dev_user_id
from constants import BOT_NAME, DEV_COMMANDS, DEVELOPER_TELEGRAM_USERNAME, PRIVATE_COMMANDS, REPOSITORY_URL, STUDIO_URL
from utils.database import *


async def start(update: Update, context: CallbackContext):
    USERNAME = 0
    # Initialize user_data
    context.user_data["message_to_delete"] = []
    if not context.user_data.__contains__("logged_in"):
        keyboard_lan = [
            [
                InlineKeyboardButton("注 册", url="https://www.instapaper.com/"),
                InlineKeyboardButton("登 录", callback_data="login_confirm"),
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard_lan)
        await update.effective_message.reply_text(
            f"欢迎使用 {BOT_NAME}！\n开始使用前，请先登录您的账号。", reply_markup=markup
        )
        return USERNAME
    else:
        await update.effective_message.reply_text(
            text="您已登录，可以直接使用！",
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton("查看文章列表", switch_inline_query_current_chat="#")
            ),
        )
        return ConversationHandler.END


async def quit_(update: Update, context: CallbackContext):
    CONFIRM_QUIT = 0
    END = -1
    if context.user_data.__contains__("logged_in"):
        keyboard = [
            [
                InlineKeyboardButton("返 回", callback_data="cancel_quit"),
                InlineKeyboardButton("解 绑", callback_data="confirm_quit"),
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.effective_message.reply_text(
            "确认解绑账号吗？这将会清除您在本机器人中所有的数据。", reply_markup=markup
        )
        return CONFIRM_QUIT
    else:
        await update.effective_message.reply_text("你还没有登录～\n点击开始：/start")
        return END


async def about(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("源 代 码", url=REPOSITORY_URL),
            InlineKeyboardButton("工 作 室", url=STUDIO_URL),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_markdown(
        (
            f"*{BOT_NAME}*  `{meta['version']}`\n"
            "保存消息中的链接到你的 Instapaper。\n\n"
            f"作者： @{DEVELOPER_TELEGRAM_USERNAME}\n"
            f"运行日志： @instasaverlog"
        ),
        reply_markup=markup,
    )


async def get_users(update: Update, context: CallbackContext):
    with db.atomic():
        users = User.select()
    text = ""
    for user in users[:10]:
        text += f"{user.username}  {user.id}\n"
    await update.message.reply_text(text or "还没有用户")

async def init_commands(update: Update, context: CallbackContext):
    set_commands = context.bot.set_my_commands
    await set_commands(
        commands = PRIVATE_COMMANDS,
        scope = BotCommandScopeAllPrivateChats()
    )
    await set_commands(
        commands = DEV_COMMANDS, 
        scope = BotCommandScopeChat(chat_id=dev_user_id)
    )
    await set_commands(
        commands = [],
        scope = BotCommandScopeAllGroupChats()
    )
    await update.message.reply_text("初始化命令范围成功！")

async def get_chat_id(update: Update, context: CallbackContext):
    await update.message.reply_text(update.effective_chat.id)