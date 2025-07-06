"""
Entry point for Trace-AI application
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n=== Trace-AI Starting ===")
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        if not rule.rule.startswith('/static'):
            print(f"  {rule.rule} -> {rule.endpoint}")
    print("\nServer starting at http://localhost:5000")
    print("API docs available at http://localhost:5000/docs")
    print("========================\n")
    app.run(host='0.0.0.0', port=5000)