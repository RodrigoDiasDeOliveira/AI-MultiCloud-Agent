# Dockerfile

FROM python:3.12-slim

# Instala uv (gerenciador de pacotes ultra-rápido)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copia arquivos de dependências primeiro (melhor cache)
COPY pyproject.toml uv.lock* ./

# Instala dependências
RUN uv sync --frozen --no-dev

# Copia o código fonte
COPY src/ ./src/

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD uv run python -c "import httpx; httpx.get('http://localhost:8000/health', timeout=5)" || exit 1

# Comando padrão
CMD ["uv", "run", "src/ai_multicloud_agent/main.py", "run", "--host", "0.0.0.0"]