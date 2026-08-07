import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("لازم تحط GROQ_API_KEY و TELEGRAM_BOT_TOKEN في ملف .env")

CHROMA_DIR = "./chroma_db"
KNOWLEDGE_FILE = "knowledge.txt"
MEMORY_DB = "agent_memory.db"

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL = "llama-3.3-70b-versatile"