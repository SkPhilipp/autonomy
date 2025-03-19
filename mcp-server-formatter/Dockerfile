FROM python:3.12-slim-bookworm

WORKDIR /app
RUN mkdir -p /projects

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . ./

ENTRYPOINT ["uv", "run", "mcp", "run", "main.py"]
