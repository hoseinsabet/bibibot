import os
import random
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode

# ---------- تنظیمات ----------
TOKEN = os.getenv("TOKEN")
CHANNELS = ["@bmaryamfal", "@shamtrapp"]
SUPPORT = "@thesabet"

# ---------- فال‌ها ----------
daily_fals = [
    "✨ امروز انرژی‌های مثبتی اطرافت هست. با اعتماد بنفس جلو برو.",
    "🌙 امروز یک خبر آرامش‌بخش می‌شنوی.",
    "🔥 یک تصمیم مهم امروز باید گرفته شود. نترس، موفق می‌شوی.",
    "🌼 روزی پر از اتفاقات کوچک اما لذت‌بخش برایت رقم می‌خورد.",
]

weekly_fals = [
    "🔮 این هفته مسیرهای تازه‌ای برایت باز می‌شود.",
    "🌟 در این هفته شخصی که انتظارش را نداشتی به تو نزدیک می‌شود.",
    "💫 این هفته یک فرصت مالی کوچک برایت پیش می‌آید.",
]

monthly_fals = [
    "📅 این ماه تغییری بزرگ در زندگی‌ات رخ می‌دهد.",
    "🌓 این ماه دوران آرامش بیشتری خواهی داشت.",
    "🌞 ماهی پر از امید، اتفاقات خوب و حرکت‌های مثبت در پیش داری.",
]

# ---------- منوها ----------
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔮 فال روزانه", callback_data="daily_fal")],
        [InlineKeyboardButton("🗓 فال هفتگی", callback_data="weekly_fal")],
        [InlineKeyboardButton("📅 فال ماهانه", callback_data="monthly_fal")],
        [InlineKeyboardButton("📜 انواع فال", callback_data="fal_menu")],
        [InlineKeyboardButton("💎 عضویت VIP", callback_data="vip")],
        [InlineKeyboardButton("📆 رزرو فال شخصی", callback_data="reserve")],
        [InlineKeyboardButton("ℹ️ درباره ما", callback_data="about")],
        [InlineKeyboardButton("🛠 پشتیبانی", callback_data="support")],
    ])

def fal_types_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔮 فال تاروت", callback_data="tarot")],
        [InlineKeyboardButton("☕ فال قهوه", callback_data="coffee")],
        [InlineKeyboardButton("🕯 فال شمع", callback_data="candle")],
        [InlineKeyboardButton("📖 فال حافظ", callback_data="hafez")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back")],
    ])

# ---------- چک عضویت ----------
async def check_join(user_id, bot):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user_id)
            if member.status == "left":
                return False
        except:
            return False
    return True

# ---------- استارت ----------
async def start(update, context):
    user = update.effective_user

    if not await check_join(user.id, context.bot):
        return await update.message.reply_text(
            "🚫 برای استفاده از ربات ابتدا در کانال‌ها عضو شوید:\n\n"
            "📌 @bmaryamfal\n📌 @shamtrapp\n\n"
            "بعد از عضویت، روی دکمه زیر بزنید 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✔ عضو شدم", callback_data="check")],
                [InlineKeyboardButton("📌 عضویت در کانال اول", url="https://t.me/bmaryamfal")],
                [InlineKeyboardButton("📌 عضویت در کانال دوم", url="https://t.me/shamtrapp")],
            ])
        )

    await update.message.reply_text(
        f"🌸 خوش اومدی {user.first_name} عزیز!\nیک گزینه را انتخاب کن:",
        reply_markup=main_menu()
    )

# ---------- دکمه‌ها ----------
async def buttons(update: Update, context):
    query = update.callback_query
    await query.answer()

    # چک عضویت
    if query.data == "check":
        if not await check_join(query.from_user.id, context.bot):
            return await query.edit_message_text(
                "❌ هنوز عضو کانال‌ها نشده‌اید!\n\n"
                "📌 @bmaryamfal\n📌 @shamtrapp",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✔ عضو شدم", callback_data="check")],
                ])
            )
        else:
            return await query.edit_message_text("✔ تایید شد! حالا می‌تونی از ربات استفاده کنی:", reply_markup=main_menu())

    # بازگشت
    if query.data == "back":
        return await query.edit_message_text("منوی اصلی:", reply_markup=main_menu())

    # فال‌ها
    if query.data == "daily_fal":
        return await query.edit_message_text("🔮 *فال امروز:*\n\n" + random.choice(daily_fals), parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu())
    if query.data == "weekly_fal":
        return await query.edit_message_text("🗓 *فال هفتگی:*\n\n" + random.choice(weekly_fals), parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu())
    if query.data == "monthly_fal":
        return
