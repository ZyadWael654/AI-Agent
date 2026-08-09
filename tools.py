from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from rag import get_retriever
from config import TAVILY_API_KEY
from config import llm_vision
from langchain_core.messages import HumanMessage

# الـ retriever بيتحمل مرة واحدة بس لما الملف ده يتستورد
retriever = get_retriever()


@tool
def search_knowledge_base(query: str) -> str:
    """تُستخدم للبحث في قاعدة المعرفة عن خدمات المكان، المنيو، المنتجات، الأسعار، مواعيد العمل، التوصيل، وطرق الدفع."""
    results = retriever.invoke(query)
    if not results:
        print(f"\n[DEBUG - No results found for]: {query}\n")
        return "معنديش معلومات عن السؤال ده في قاعدة المعرفة."

    context = "\n---\n".join([doc.page_content for doc in results])
    print(f"\n[DEBUG - Executed Knowledge Search]:\n{context}\n")
    return context


@tool
def get_weather(city: str) -> str:
    """تُستخدم لمعرفة حالة الطقس ودرجة الحرارة في مدينة معينة."""
    return f"درجة الحرارة في {city} حالياً هي 25 درجة مئوية والطقس مشمس."


# إنشاء Instance من Tavily لاستخدامه جوه الأداة
tavily_instance = TavilySearchResults(
    max_results=3,
    tavily_api_key=TAVILY_API_KEY
)


@tool
def web_search(query: str) -> str:
    """تُستخدم للبحث في الإنترنت عن الأخبار العامة والأحداث والمعلومات الخارجة عن قاعدة المعرفة."""
    results = tavily_instance.invoke({"query": query})
    return str(results)


tools = [search_knowledge_base, get_weather, web_search]
def analyze_image(image_base64: str) -> str:
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    "حلل الصورة دي في جزئين منفصلين:\n\n"
                    "1) وصف عام مختصر (سطر أو اتنين بس): إيه الصورة دي؟\n\n"
                    "2) النص المستخرج (OCR): انسخ كل سطر نص أو رقم موجود في الصورة "
                    "بالظبط زي ما هو مكتوب، سطر تحت سطر، من غير تلخيص أو حذف أي رقم. "
                    "لو فيه جدول أسعار أو منتجات، اكتب كل منتج وسعره في سطر منفصل زي:\n"
                    "اسم المنتج - السعر\n\n"
                    "لو مفيش نص خالص في الصورة، قول بوضوح: لا يوجد نص في هذه الصورة.\n"
                    "رد بالعربي، والأرقام سيبها زي ما هي بالإنجليزي."
                ),
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
            },
        ]
    )
    try:
        response = llm_vision.invoke([message])
        return response.content
    except Exception as e:
        return f"معرفتش أحلل الصورة دي: {e}"