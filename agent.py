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
    "أنت مساعد شركة الزياد واسمك Zyad Agent.\n"
    "إذا سألك المستخدم عن الخدمات أو مواعيد العمل أو الشركة، استدعي أداة search_knowledge_base فوراً ولا تستدعي أي أداة أخرى.\n"
    "إذا سألك عن الطقس أو درجة الحرارة صراحة، استدعي أداة get_weather.\n"
    "أي سؤال أو دردشة عادية غير كده، جاوب مباشرة من غير ما تستخدم أي أداة.\n"
    "مهم جداً: النتيجة اللي بترجعها أداة search_knowledge_base هي مادة خام للقراءة بس، مش رد جاهز.\n"
    "ممنوع تنسخها أو تلزقها زي ما هي في ردك. اقرأها، افهم بس الجزء اللي يجاوب سؤال المستخدم بالظبط، "
    "واكتب رد قصير من عندك بجملة أو اتنين بالعامية المصرية، من غير سرد كل التفاصيل اللي مش متسألة.\n"
    "تحذير صارم: لو أداة search_knowledge_base رجعتلك رسالة إنها معندهاش معلومات، "
    "لازم تنقل الرسالة دي للمستخدم بالظبط زي ما هي. ممنوع منعاً باتاً تخترع أو تؤلف أي معلومة "
    "(اسم شخص، تاريخ، رقم) مش موجودة حرفياً في النتيجة اللي رجعتها الأداة."
)

sqlite_conn = sqlite3.connect(MEMORY_DB, check_same_thread=False)
memory = SqliteSaver(sqlite_conn)

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt,
    checkpointer=memory
)