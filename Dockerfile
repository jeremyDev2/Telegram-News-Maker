FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen
COPY . .
CMD ["uv", "run", "granian", "--interface", "asgi", "main:app", "--host", "0.0.0.0", "--port", "8000"]
