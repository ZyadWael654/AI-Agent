import sqlite3
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver

from config import GROQ_API_KEY, LLM_MODEL, MEMORY_DB
from tools import tools


llm = ChatGroq(
    model_name=LLM_MODEL,
    temperature=0.1,
    groq_api_key=GROQ_API_KEY
)

system_prompt = (
    "أنت مساعد ذكي ومحترف اسمه Zyad Agent.\n\n"
    "قواعد استخدام الأدوات ورأي الأولويات:\n"
    "1. تحدث دائماً بالعامية المصرية الروشة والمبسطة.\n"
    "2. إذا كان السؤال عن شركة الزياد أو خدماتها أو مواعيدها -> استخدم أداة search_knowledge_base أولاً.\n"
    "3. إذا كان السؤال عن معلومات موسوعية، تاريخية، شخصيات، أو تعريفات عامة -> استخدم أداة wikipedia_search.\n"
    "4. إذا كان السؤال عن أخبار حديثة، مباريات، أحداث جارية، أو شيء غير موجود في قاعدة المعرفة -> استخدم أداة web_search.\n"
    "5. لا تستدعي get_weather إلا عند السؤال الصريح عن حالة الجو أو الطقس."
)

sqlite_conn = sqlite3.connect(MEMORY_DB, check_same_thread=False)
memory = SqliteSaver(sqlite_conn)

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt,
    checkpointer=memory
)