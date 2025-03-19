FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install uv

COPY pyproject.toml uv.lock* ./
RUN uv pip install --system .

COPY . /app

ENTRYPOINT ["python", "-m", "mcp", "run", "main.py"]
# run --env-file={PATH_TO_YOUR_PROJECT}/.env mcp run main.py
