from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from config import llm, MEMORY_DB
from tools import tools
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "أنت مساعد خدمة عملاء كافيه Brew & Co واسمك Brew Bot.\n\n"
     "قواعد الإجابة:\n"
     "1. للأسئلة المتعلقة بالكافيه (المنيو، الأسعار، المواعيد، التوصيل، طرق الدفع): استخدم أداة search_knowledge_base.\n"
     "2. 'المنتجات المتاحة' في نتيجة البحث هي المنيو المتاح والأسعار، اذكرها للمستخدم مباشرة عند السؤال عن المنيو أو الأسعار.\n"
     "3. لا تستخدم أداة web_search لأسئلة الكافيه إطلاقاً.\n"
     "4. إذا لم تجد المعلومة في نتيجة البحث (مثل اسم المالك)، قل بوضوح: 'معنديش معلومات عن الموضوع ده'."
    ),
    MessagesPlaceholder(variable_name="messages"),
])

sqlite_conn = sqlite3.connect(MEMORY_DB, check_same_thread=False)
memory = SqliteSaver(sqlite_conn)

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=prompt,
    checkpointer=memory
)