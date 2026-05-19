# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY cron/ ./cron/

# Setup cron job
RUN chmod 0644 cron/2fa-cron && \
    crontab cron/2fa-cron

# Create volume mount points
RUN mkdir -p /data /cron && \
    chmod 755 /data /cron

EXPOSE 8080

# Start cron and application
CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8080
