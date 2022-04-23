from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ApiIdInvalid,    PhoneNumberInvalid,    PhoneCodeInvalid,    PhoneCodeExpired,    SessionPasswordNeeded,    PasswordHashInvalid
from telethon.errors import ApiIdInvalidError,    PhoneNumberInvalidError,    PhoneCodeInvalidError,    PhoneCodeExpiredError,    SessionPasswordNeededError,    PasswordHashInvalidError
ERROR_MESSAGE = "- عـذراً حدث خطأ ! \n\n**خطأ !** : {} " \
            "\n\n- يرجى ابلاغي اذا كان هناك خطأ  @KFFF6 " \
            "معلومات حساسة وأنت إذا كنت تريد الإبلاغ عن هذا كـ" \
            "لم يتم تسجيل رسالة الخطأ هذه بواسطتنا!"
@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "**- اضغـط علـى زر بـدء ⌬...**",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("بـدء استخـراج كـود تيرمكـس", callback_data="EVI")
        ]])
    )
async def generate_session(bot, msg, telethon=False):
    await msg.reply("بـدء {} استخـراج الجلسـه ⌬....".format("سييي" if telethon else "Pyrogram"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, '**- حسنـا الان يرجى ارسـال كـود API_ID**', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('API_ID غير صحيح (والذي يجب أن يكون عددًا صحيحًا). يرجى البدء في إنشاء الجلسة مرة أخرى.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, '**- حسنـا الان يرجى ارسـال كـود API_HASH**', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, '- الان يرجى ارسال رقمك بشكل كامل \nمثال : `+964xxxxxxx`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("**- جـاري ارسـال الكـود لحـافظـة حسـابك ⎙...**")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('- عذرا معلومات ال API_HASH وال API_ID غير صالحة يرجى اعادة الخطوات كامله .', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('- رقم هاتفك غير صالح ! يرجى اعادة الخطوات كامله .', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "**- قم بادخال الكود الذي وصل اليك من الشركة ( كود الدخول ) ، أرسل كود الدخول بالتنسيق التالي:**\n- اذا كان الكود  هو ``12345`` يرجى ارسالـه بالشكـل التالي ``1 2 3 4 5`` مع وجود مسـافـات بين الارقام\n\n**- اذا احتجت مساعدة** @KFFF6 .", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('بلغ الحد الزمني 10 دقائق. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('OTP غير صالح. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('انتهت صلاحية كلمة المرور لمرة واحدة. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, '**- قـم بادخـال كلمـة مـرور حسابـك ( التحقق بـ خطوتين ).**', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('بلغ الحد الزمني 5 دقائق. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('- أدخلت كلمة مرور غير صالحة. يرجى البدء في إنشاء الجلسة مرة أخرى.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} كود تيرمكس** \n\n`{}` \n\تم الاستخـراج بواسطـة @R125R".format("ZEDThon" if telethon else "PYROGRAM", string_session)
    await client.send_message("me", text)
    await client.disconnect()
    await phone_code_msg.reply("تم الاستخـراج بنجاح {} كود تيرمكس. \n\nالرجـاء التحـقق مـن حافظـة حسـابك! \n\nبواسطـة @KFFF6".format("E125E" if telethon else "pyrogram"))
async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("- تم الالغاء .", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("- تتم اعادة تشغيل البوت .", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("- تم الغاء عملية الاستخراج .", quote=True)
        return True
    else:
        return False


# @Client.on_message(filters.private & ~filters.forwarded & filters.command(['cancel', 'restart']))
# async def formalities(_, msg):
#     if "/cancel" in msg.text:
#         await msg.reply("Membatalkan Semua Processes!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     elif "/restart" in msg.text:
#         await msg.reply("Memulai Ulang Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     else:
#         return False
