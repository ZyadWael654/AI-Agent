from agent import agent
import time


test_cases = [
    {
        "question": "عندكم إيه في المنيو؟",
        "expected_keywords": ["اسبريسو", "كابتشينو", "لاتيه"]
    },
    {
        "question": "سعر الكابتشينو كام؟",
        "expected_keywords": ["55"]
    },
    {
        "question": "سعر التشيز كيك كام؟",
        "expected_keywords": ["70"]
    },
    {
        "question": "مواعيد العمل عندكم إيه؟",
        "expected_keywords": ["8", "11"]
    },
    {
        "question": "فيه توصيل؟",
        "expected_keywords": ["5", "20", "استلام"]
    },
    {
        "question": "تقدروا تدفعوا بفيزا؟",
        "expected_keywords": ["فيزا"]
    },
    {
    "question": "مين مالك الكافيه؟",
    "expected_keywords": ["معنديش", "مش موجود", "معندهاش", "لا يوجد", "معندكش"]
    },
]


def run_evaluation():
    passed = 0
    failed = 0

    print("=" * 50)
    print("بدء تقييم الـ RAG - Brew & Co")
    print("=" * 50)

    for i, case in enumerate(test_cases, 1):
        
        config = {"configurable": {"thread_id": f"test_run_{time.time()}_{i}"}}
        
        try:
            response = agent.invoke(
                {"messages": [("user", case["question"])]},
                config=config
            )
            answer = response["messages"][-1].content
        except Exception as e:
            answer = f"[خطأ في الاستدعاء: {e}]"

        normalized_answer = answer.replace(" ", "").replace("ـ", "")
        found = any(
            keyword.replace(" ", "") in normalized_answer
            for keyword in case["expected_keywords"]
        )

        status = "✅ PASS" if found else "❌ FAIL"
        if found:
            passed += 1
        else:
            failed += 1

        print(f"\n[{i}] {status}")
        print(f"السؤال: {case['question']}")
        print(f"الرد: {answer}")
        print(f"الكلمات المتوقعة: {case['expected_keywords']}")

        time.sleep(3)  

    print("\n" + "=" * 50)
    print(f"النتيجة النهائية: {passed} نجح / {failed} فشل من أصل {len(test_cases)}")
    print("=" * 50)


if __name__ == "__main__":
    run_evaluation()