from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
@Client.on_message(filters.private & filters.incoming & filters.command("help"))
async def _help(bot, msg):
    await bot.send_message(        msg.chat.id,        "**طـريقـة استخـدام البـوت **\n" + Data.HELP,        reply_markup=InlineKeyboardMarkup(Data.home_buttons)    )
