# Base image
FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install --no-cache-dir -r requirements.txt


# Copy wait script
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Expose port
EXPOSE 8000

# Run server (IMPORTANT: use wait-for-it)
CMD ["/wait-for-it.sh", "db", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]