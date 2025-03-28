FROM python:3.12-slim-bookworm

WORKDIR /app
RUN mkdir -p /projects

# Install lynx browser and its dependencies
RUN apt-get update && apt-get install -y \
    lynx \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . ./

ENTRYPOINT ["uv", "run", "mcp", "run", "main.py"]
