# FASTAPI BUGBYTES SERIES


uv init fastapi-bugbytes

cd fastapi-bugbytes/

uv venv

uv add fastapi "uvicorn[standard]" psycopg2-binary sqlmodel

uv run uvicorn main:app --reload --port 8090


#### docs
http://localhost:8090/docs

#### redocs
http://localhost:8090/redoc