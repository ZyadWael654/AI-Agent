import sqlite3

# إنشاء أو الاتصال بقاعدة البيانات المحلية
DB_NAME = "agent_memory.db"

def init_db():
    """إنشاء الجدول الخاص بحفظ الجلسات والمحادثات لو مش موجود"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_message(session_id: str, role: str, content: str):
    """حفظ رسالة واحدة (user أو assistant أو tool) في قاعدة البيانات"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, str(content))
    )
    conn.commit()
    conn.close()

def load_history(session_id: str) -> list:
    """استرجاع المحادثات القديمة الخاصة بـ session_id معين"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY id ASC", 
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for role, content in rows:
        history.append({"role": role, "content": content})
    return history