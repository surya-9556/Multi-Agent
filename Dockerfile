FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /src

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python -m ensurepip --upgrade \
    && python -m pip install --no-cache-dir uv \
    && uv pip install --system --no-cache-dir -e .

EXPOSE 8501
EXPOSE 8080

CMD ["uv", "run", "main"]