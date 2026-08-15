import time
from collections import defaultdict

MAX_REQUESTS = 5     
TIME_WINDOW = 60        

user_requests = defaultdict(list)


def is_rate_limited(chat_id: str) -> bool:
    """
    بترجع True لو المستخدم تعدى الحد المسموح، وFalse لو لسه مسموحله.
    """
    now = time.time()
    timestamps = user_requests[chat_id]

    timestamps[:] = [t for t in timestamps if now - t < TIME_WINDOW]

    if len(timestamps) >= MAX_REQUESTS:
        return True

    timestamps.append(now)
    return False