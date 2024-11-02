FROM python:3.12.4-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m unittest test.py

COPY app/. ./

CMD ["python", "-m", "app"]
