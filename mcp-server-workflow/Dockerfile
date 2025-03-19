FROM python:3.12-slim-bookworm

WORKDIR /app
RUN mkdir -p /projects

RUN pip install uv

# install git
RUN apt-get update && apt-get install -y git wget && rm -rf /var/lib/apt/lists/*

# install gh
RUN mkdir -p -m 755 /etc/apt/keyrings && \
    wget -O- https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . ./

ENTRYPOINT ["uv", "run", "mcp", "run", "main.py"]
