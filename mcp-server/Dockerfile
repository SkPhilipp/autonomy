FROM python:3.12-slim-bookworm

WORKDIR /app
RUN mkdir -p /project

RUN pip install uv

# install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . ./

ENTRYPOINT ["uv", "run", "mcp", "run", "main.py"] 