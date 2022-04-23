import Config
import logging
from pyromod import listen
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid


logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


app = Client(
    ":memory:",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="StringSessionBot"),
)


# Run Bot
if __name__ == "__main__":
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("API_ID / API_HASH الخاص بك غير صالح.")
    except AccessTokenInvalid:
        raise Exception("BOT_TOKEN الخاص بك غير صالح.")
    uname = app.get_me().username
    print(f"@{uname} بدأت بنجاح!")
    idle()
    app.stop()
    print("توقف الروبوت. ألفيدا!")
