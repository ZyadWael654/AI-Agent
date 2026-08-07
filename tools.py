from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from rag import get_retriever
from config import TAVILY_API_KEY

# الـ retriever بيتحمل مرة واحدة بس لما الملف ده يتستورد
retriever = get_retriever()


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


web_search = TavilySearch(max_results=3, tavily_api_key=TAVILY_API_KEY, topic="general")
tools = [search_knowledge_base, get_weather, web_search]