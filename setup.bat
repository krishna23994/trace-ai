@echo off
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example
)
echo Setup complete! Run 'python app.py' or 'py app.py' to start the server.