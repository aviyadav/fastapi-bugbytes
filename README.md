# FASTAPI BUGBYTES SERIES


uv init fastapi-bugbytes

cd fastapi-bugbytes/

uv venv

uv add fastapi "uvicorn[standard]"

uv run uvicorn main:app --reload