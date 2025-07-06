"""
Database operations for Trace-AI
"""
import sqlite3
from typing import List, Dict, Optional


def init_db(db_path: str) -> None:
    """Initialize SQLite database with logs table"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trace_id TEXT NOT NULL,
            message TEXT NOT NULL,
            level TEXT DEFAULT 'INFO',
            timestamp TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def store_log(db_path: str, trace_id: str, message: str, level: str = 'INFO', timestamp: Optional[str] = None) -> None:
    """Store a log entry in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (trace_id, message, level, timestamp) VALUES (?, ?, ?, ?)",
        (trace_id, message, level, timestamp)
    )
    conn.commit()
    conn.close()


def get_logs_by_trace(db_path: str, trace_id: str) -> List[Dict]:
    """Retrieve all logs for a trace ID"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT message, level, timestamp FROM logs WHERE trace_id = ? ORDER BY created_at",
        (trace_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [{"message": r[0], "level": r[1], "timestamp": r[2]} for r in rows]


def get_log_messages_by_trace(db_path: str, trace_id: str) -> List[str]:
    """Get log messages for a trace (for summarization)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM logs WHERE trace_id = ?", (trace_id,))
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()
    return messages


def delete_all_logs(db_path: str) -> int:
    """Delete all logs"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count


def delete_logs_by_trace(db_path: str, trace_id: str) -> int:
    """Delete logs by trace ID"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs WHERE trace_id = ?", (trace_id,))
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count


def delete_logs_by_timestamp(db_path: str, before: Optional[str] = None, after: Optional[str] = None) -> int:
    """Delete logs by timestamp range"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if before and after:
        cursor.execute("DELETE FROM logs WHERE timestamp BETWEEN ? AND ?", (after, before))
    elif before:
        cursor.execute("DELETE FROM logs WHERE timestamp < ?", (before,))
    elif after:
        cursor.execute("DELETE FROM logs WHERE timestamp > ?", (after,))
    else:
        return 0
    
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count