FROM python:3.12.4-slim-bookworm

WORKDIR /app

# Install necessary system libraries
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files, including service_account.json
COPY app/. ./

CMD ["python", "-m", "app"]
