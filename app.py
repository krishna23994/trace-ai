from flask import Flask, request, jsonify
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DB_PATH = os.getenv("DB_PATH")

# --- DB Setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trace_id TEXT,
            message TEXT,
            level TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- API Endpoints ---

@app.route("/logs", methods=["POST"])
def receive_log():
    data = request.json
    trace_id = data.get("trace_id")
    message = data.get("message")
    level = data.get("level", "INFO")
    timestamp = data.get("timestamp")

    if not trace_id or not message:
        return jsonify({"error": "trace_id and message are required"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (trace_id, message, level, timestamp) VALUES (?, ?, ?, ?)",
                   (trace_id, message, level, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"status": "log stored"}), 200


@app.route("/logs/<trace_id>", methods=["GET"])
def get_logs(trace_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT message, level, timestamp FROM logs WHERE trace_id = ?", (trace_id,))
    rows = cursor.fetchall()
    conn.close()

    logs = [{"message": r[0], "level": r[1], "timestamp": r[2]} for r in rows]
    return jsonify({"trace_id": trace_id, "logs": logs})


@app.route("/summarize/<trace_id>", methods=["GET"])
def summarize_logs(trace_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM logs WHERE trace_id = ?", (trace_id,))
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not messages:
        return jsonify({"error": "No logs found"}), 404

    # Example: Basic mock summarization
    summary = f"This trace has {len(messages)} log entries. Sample log: {messages[0][:100]}..."

    return jsonify({"trace_id": trace_id, "summary": summary})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
