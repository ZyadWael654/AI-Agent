from telegram import Update
from telegram.ext import ContextTypes

from agent import agent


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا Zyad AI Agent. كيف يمكنني مساعدتك اليوم؟")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = str(update.effective_chat.id)

    config = {"configurable": {"thread_id": chat_id}}

    try:
        response = agent.invoke(
            {"messages": [("user", user_text)]},
            config=config
        )

        bot_reply = response["messages"][-1].content
        await update.message.reply_text(bot_reply)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("حدث خطأ بسيط، جرب مرة أخرى.")