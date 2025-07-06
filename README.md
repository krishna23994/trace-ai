# Trace-AI

Log collection and analysis API with trace correlation.

## Features

- **Log Collection** - REST API for storing structured log entries
- **Trace Correlation** - Group related logs using trace IDs
- **Log Retrieval** - Query logs by trace identifier
- **Basic Summarization** - Generate summaries of log sequences
- **SQLite Storage** - Lightweight, file-based database

## Project Structure

```
trace-ai/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database operations
│   ├── routes.py            # API endpoints
│   └── swagger.py           # OpenAPI specification
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_api.py          # Unit tests
│   └── test_e2e.py          # Integration tests
├── run.py                   # Application entry point
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## Quick Start

```bash
# Setup
pip install -r requirements.txt
setup.bat  # Windows - creates .env file

# Run
py run.py
```

**Server:** http://localhost:5000  
**Docs:** http://localhost:5000/docs

## API Endpoints

- `POST /v1/logs` - Store log entry (requires timestamp)
- `GET /v1/logs/{trace_id}` - Get logs by trace ID  
- `GET /v1/summarize/{trace_id}` - Get trace summary
- `DELETE /v1/logs?trace_id=X` - Delete by trace ID
- `DELETE /v1/logs?before=X&after=Y` - Delete by timestamp
- `DELETE /v1/logs?all=true` - Delete all logs

## Example Usage

```bash
# Store a log
curl -X POST http://localhost:5000/v1/logs \
  -H "Content-Type: application/json" \
  -d '{"trace_id":"user-123","message":"Login started","level":"INFO","timestamp":"2024-01-01T10:00:00Z"}'

# Get logs
curl http://localhost:5000/v1/logs/user-123

# Get summary
curl http://localhost:5000/v1/summarize/user-123

# Delete by trace ID
curl -X DELETE "http://localhost:5000/v1/logs?trace_id=user-123"
```

## Testing

```bash
# Run all tests
py -m pytest

# Run with verbose output
py -m pytest -v

# Run specific test file
py -m pytest tests/test_api.py -v

# Run with coverage (install: pip install pytest-cov)
py -m pytest --cov=app --cov-report=html
```

## Development

### Environment Variables
Edit `.env` file:
```bash
DB_PATH=logs.db              # Database file path
SECRET_KEY=your-secret-key   # Flask secret key
```

### Common Commands
```bash
# Start server
py run.py

# Start with debug mode (development)
FLASK_ENV=development py run.py

# Clean database
del logs.db  # Windows
rm logs.db   # Linux/Mac

# Install new dependencies
pip install package-name
pip freeze > requirements.txt
```