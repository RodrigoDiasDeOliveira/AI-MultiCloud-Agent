FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --upgrade pip \
    && pip install "hatchling>=1.17.0" \
    && pip install .
COPY . .
CMD ["uvicorn", "ai_multicloud_agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
