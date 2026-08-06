import time
from collections import defaultdict

# إعدادات الحد المسموح به
MAX_REQUESTS = 5       # أقصى عدد رسايل
TIME_WINDOW = 60        # خلال 60 ثانية (دقيقة)

# قاموس بيخزن أوقات الطلبات لكل مستخدم
user_requests = defaultdict(list)


def is_rate_limited(chat_id: str) -> bool:
    """
    بترجع True لو المستخدم تعدى الحد المسموح، وFalse لو لسه مسموحله.
    """
    now = time.time()
    timestamps = user_requests[chat_id]

    # امسح أي طلبات قديمة أقدم من الـ TIME_WINDOW
    timestamps[:] = [t for t in timestamps if now - t < TIME_WINDOW]

    if len(timestamps) >= MAX_REQUESTS:
        return True

    timestamps.append(now)
    return False