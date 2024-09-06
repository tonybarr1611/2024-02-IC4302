FROM python:3.12.4-slim-bookworm

WORKDIR /app

# Install necessary system libraries
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/. .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "flask",  "--app", "app", "run" ]
