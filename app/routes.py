"""
API routes for Trace-AI log collection and analysis
"""
from flask import Blueprint, request, jsonify, current_app
from app.database import store_log, get_logs_by_trace, get_log_messages_by_trace, delete_all_logs, delete_logs_by_trace, delete_logs_by_timestamp

logs_bp = Blueprint('logs', __name__)


@logs_bp.route('/v1/logs', methods=['POST'])
def create_log():
    """Store a new log entry"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    
    trace_id = data.get("trace_id")
    message = data.get("message")
    level = data.get("level", "INFO")
    timestamp = data.get("timestamp")
    
    if not trace_id or not message or not timestamp:
        return jsonify({"error": "trace_id, message, and timestamp are required"}), 400
    
    store_log(current_app.config['DB_PATH'], trace_id, message, level, timestamp)
    return jsonify({"status": "log stored"}), 200


@logs_bp.route('/v1/logs/<trace_id>', methods=['GET'])
def get_trace_logs(trace_id):
    """Retrieve all logs for a trace ID"""
    logs = get_logs_by_trace(current_app.config['DB_PATH'], trace_id)
    return jsonify({"trace_id": trace_id, "logs": logs})


@logs_bp.route('/v1/summarize/<trace_id>', methods=['GET'])
def summarize_trace_logs(trace_id):
    """Generate summary of logs for a trace ID"""
    messages = get_log_messages_by_trace(current_app.config['DB_PATH'], trace_id)
    
    if not messages:
        return jsonify({"error": "No logs found"}), 404
    
    # Basic summarization - can be enhanced with AI in future
    summary = f"This trace has {len(messages)} log entries. Sample log: {messages[0][:100]}..."
    
    return jsonify({"trace_id": trace_id, "summary": summary})


@logs_bp.route('/v1/logs', methods=['DELETE'])
def delete_logs():
    """Delete logs by various criteria"""
    trace_id = request.args.get('trace_id')
    before = request.args.get('before')
    after = request.args.get('after')
    delete_all = request.args.get('all')
    
    if delete_all == 'true':
        count = delete_all_logs(current_app.config['DB_PATH'])
    elif trace_id:
        count = delete_logs_by_trace(current_app.config['DB_PATH'], trace_id)
    elif before or after:
        count = delete_logs_by_timestamp(current_app.config['DB_PATH'], before, after)
    else:
        return jsonify({"error": "Specify trace_id, timestamp (before/after), or all=true"}), 400
    
    return jsonify({"deleted": count})