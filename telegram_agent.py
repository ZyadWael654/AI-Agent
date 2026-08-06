import os
import shutil
import warnings
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()

# ==========================================
# 0. API Keys Setup (من .env دلوقتي)
# ==========================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not GROQ_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("لازم تحط GROQ_API_KEY و TELEGRAM_BOT_TOKEN في ملف .env")

# ==========================================
# 1. RAG System Setup (منبنيهوش من الصفر لو موجود بالفعل)
# ==========================================
print("=== Initializing Vector Database (RAG)... ===")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

CHROMA_DIR = "./chroma_db"
KNOWLEDGE_FILE = "knowledge.txt"

# لو مفيش قاعدة بيانات موجودة، ابنيها من الملف. لو موجودة، استخدمها زي ما هي.
if not os.path.exists(CHROMA_DIR):
    print("=== No existing DB found, building from knowledge.txt... ===")
    loader = TextLoader(KNOWLEDGE_FILE, encoding="utf-8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=0,
    separators=["\n\n", "\n"]
)

    docs = text_splitter.split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
else:
    print("=== Loading existing Vector Database... ===")
    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

retriever = vector_store.as_retriever(search_kwargs={"k":1 })

print("=== Vector Database Ready! ===")

# ==========================================
# 2. Tools Definition
# ==========================================
@tool
def search_knowledge_base(query: str) -> str:
    """استخدم هذه الأداة للإجابة عن أسئلة شركة الزياد، الخدمات المتاحة، ومواعيد العمل وسياسة الدعم."""
    results = retriever.invoke(query)
    if not results:
        print(f"\n[DEBUG - No results found for]: {query}\n")
        return "معنديش معلومات عن السؤال ده في قاعدة المعرفة."

    context = "\n---\n".join([doc.page_content for doc in results])
    print(f"\n[DEBUG - Executed Knowledge Search]:\n{context}\n")
    return context

@tool
def get_weather(city: str) -> str:
    """استخدم هذه الأداة فقط وفقط إذا احتوت رسالة المستخدم على كلمة (طقس) أو (درجة الحرارة) أو (الجو)."""
    return f"درجة الحرارة في {city} حالياً هي 25 درجة مئوية والطقس مشمس."

tools = [search_knowledge_base, get_weather]

# ==========================================
# 3. LLM Setup
# ==========================================
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.1,
    groq_api_key=GROQ_API_KEY
)

system_prompt = (
    "أنت مساعد شركة الزياد واسمك Zyad Agent.\n"
    "إذا سألك المستخدم عن الخدمات أو مواعيد العمل أو الشركة، استدعي أداة search_knowledge_base فوراً ولا تستدعي أي أداة أخرى.\n"
    "إذا سألك عن الطقس أو درجة الحرارة صراحة، استدعي أداة get_weather.\n"
    "أي سؤال أو دردشة عادية غير كده، جاوب مباشرة من غير ما تستخدم أي أداة.\n"
    "مهم جداً: النتيجة اللي بترجعها أداة search_knowledge_base هي مادة خام للقراءة بس، مش رد جاهز.\n"
    "ممنوع تنسخها أو تلزقها زي ما هي في ردك. اقرأها، افهم بس الجزء اللي يجاوب سؤال المستخدم بالظبط، "
    "واكتب رد قصير من عندك بجملة أو اتنين بالعامية المصرية، من غير سرد كل التفاصيل اللي مش متسألة.\n"
    "مثال: لو المستخدم سأل عن مواعيد العمل بس، جاوب بمواعيد العمل بس، متجيبش نبذة عن الشركة أو سياسة الدعم كمان."
)

# ==========================================
# 4. Persistent Memory (SQLite بدل الذاكرة المؤقتة)
# ==========================================
sqlite_conn = sqlite3.connect("agent_memory.db", check_same_thread=False)
memory = SqliteSaver(sqlite_conn)

app = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt,
    checkpointer=memory
)

# ==========================================
# 5. Telegram Bot Integration
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا Zyad AI Agent. كيف يمكنني مساعدتك اليوم؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = str(update.effective_chat.id)

    config = {"configurable": {"thread_id": chat_id}}

    try:
        response = app.invoke(
            {"messages": [("user", user_text)]},
            config=config
        )

        bot_reply = response["messages"][-1].content
        await update.message.reply_text(bot_reply)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("حدث خطأ بسيط، جرب مرة أخرى.")

if __name__ == "__main__":
    print("=== Telegram Bot Starting ===")
    telegram_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start_command))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    telegram_app.run_polling(drop_pending_updates=True)