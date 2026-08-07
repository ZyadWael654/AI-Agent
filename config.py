import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GOOGLE_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("لازم تحط GOOGLE_API_KEY و TELEGRAM_BOT_TOKEN في ملف .env")

CHROMA_DIR = "./chroma_db"
KNOWLEDGE_FILE = "knowledge.txt"
MEMORY_DB = "agent_memory.db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "gemini-1.5-flash"

# تعريف الموديل باستخدام Gemini
llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)