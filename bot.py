from telegram import Update
from telegram.ext import ContextTypes
from agent import agent
from rate_limiter import is_rate_limited
import traceback
import base64
from tools import analyze_image
from telegram.ext import Application, MessageHandler, filters, ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أنا أهلاً بك! Zyad AI Agent، كيف يمكنني مساعدتك اليوم؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = str(update.effective_chat.id)

    if is_rate_limited(chat_id):
        await update.message.reply_text("استنى شوية 🖐️ بتبعت رسائل كتير بسرعة، جرب تاني بعد دقيقة.")
        return

    config = {
        "configurable": {"thread_id": chat_id},
        "recursion_limit": 25
    }

    try:
        response = agent.invoke(
            {"messages": [("user", user_text)]},
            config=config
        )

        bot_reply = response["messages"][-1].content
        await update.message.reply_text(bot_reply)

    except Exception as e:
        traceback.print_exc()
        await update.message.reply_text("حدث خطأ بسيط، جرب مرة أخرى.")
        
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)

    if is_rate_limited(chat_id):
        await update.message.reply_text("استنى شوية 🙏 بتبعت رسايل كتير بسرعة، جرب تاني بعد دقيقة.")
        return

    try:
        # ناخد أعلى دقة متاحة للصورة
        photo_file = await update.message.photo[-1].get_file()
        downloaded_bytes = await photo_file.download_as_bytearray()

        image_base64 = base64.b64encode(downloaded_bytes).decode('utf-8')

        # تحليل الصورة
        image_description = analyze_image(image_base64)

        # النص اللي المستخدم كتبه مع الصورة (لو موجود)
        caption = update.message.caption or "من غير تعليق"

        user_input = (
            f"[المستخدم بعت صورة]\n"
            f"وصف الصورة: {image_description}\n"
            f"تعليق المستخدم: {caption}\n\n"
            f"رد على المستخدم بناءً على وصف الصورة ده وتعليقه."
        )

        config = {
            "configurable": {"thread_id": chat_id},
            "recursion_limit": 25
        }

        response = agent.invoke(
            {"messages": [("user", user_input)]},
            config=config
        )

        bot_reply = response["messages"][-1].content
        await update.message.reply_text(bot_reply)

    except Exception as e:
        traceback.print_exc()
        await update.message.reply_text(f"معرفتش أعالج الصورة، حصل خطأ: {e}")
