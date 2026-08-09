import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

CHROMA_DIR = "./chroma_db"
KNOWLEDGE_FILE = "knowledge.txt"
MEMORY_DB = "agent_memory.db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# موديل خفيف على Groq حدوده عالية جداً
LLM_MODEL = "openai/gpt-oss-120b"
llm = ChatGroq(
    model_name=LLM_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=0
)

VISION_MODEL = "qwen/qwen3.6-27b"

llm_vision = ChatGroq(
    model_name=VISION_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=0
)