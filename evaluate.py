from agent import agent

# أسئلة اختبار + كلمات مفتاحية المفروض تكون موجودة في الرد الصح
test_cases = [
    {
        "question": "مواعيد العمل عندكم إيه؟",
        "expected_keywords": ["9", "5", "الأحد", "الخميس"]
    },
    {
        "question": "إيه هي خدمات الشركة؟",
        "expected_keywords": ["ذكاء اصطناعي", "قواعد بيانات", "تطبيقات الويب"]
    },
    {
        "question": "سياسة الاسترجاع والدعم عندكم إيه؟",
        "expected_keywords": ["24", "14"]
    },
    {
        "question": "مين رئيس الشركة؟",
        "expected_keywords": ["معنديش", "مش موجود", "معندهاش", "لا يوجد"]
    },
    {
        "question": "شركة الزياد اتأسست فين ومتى؟",
        "expected_keywords": ["2026", "المنصورة"]
    },
]


def run_evaluation():
    passed = 0
    failed = 0

    print("=" * 50)
    print("بدء تقييم الـ RAG")
    print("=" * 50)

    for i, case in enumerate(test_cases, 1):
        config = {"configurable": {"thread_id": f"eval_test_{i}"}}
        response = agent.invoke(
            {"messages": [("user", case["question"])]},
            config=config
        )
        answer = response["messages"][-1].content

        normalized_answer = answer.replace(" ", "").replace("ـ", "")
        found = any(keyword.replace(" ", "") in normalized_answer for keyword in case["expected_keywords"])
        status = "✅ PASS" if found else "❌ FAIL"
        if found:
            passed += 1
        else:
            failed += 1

        print(f"\n[{i}] {status}")
        print(f"السؤال: {case['question']}")
        print(f"الرد: {answer}")
        print(f"الكلمات المتوقعة: {case['expected_keywords']}")

    print("\n" + "=" * 50)
    print(f"النتيجة النهائية: {passed} نجح / {failed} فشل من أصل {len(test_cases)}")
    print("=" * 50)


if __name__ == "__main__":
    run_evaluation()