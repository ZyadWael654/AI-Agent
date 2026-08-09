import warnings
warnings.filterwarnings("ignore")

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from bot import start_command, handle_message, handle_photo
if __name__ == "__main__":
    print("--- Telegram Bot Starting ---")
    
    # بناء تطبيق تليجرام
    telegram_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # إضافة الـ Handlers
    telegram_app.add_handler(CommandHandler("start", start_command))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    # تشغيل الـ Polling وتجاهل أي رسائل معلقة قديمة لمنع الـ Conflict
    telegram_app.run_polling(drop_pending_updates=True, close_loop=False)