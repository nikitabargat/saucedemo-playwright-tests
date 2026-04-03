# ── Builder stage ─────────────────────────────────────────
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required by Playwright
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers with dependencies
RUN playwright install --with-deps chromium firefox

# Copy project files
COPY . .

# ── Default: run all tests ────────────────────────────────
ENV BASE_URL=https://www.saucedemo.com \
    HEADLESS=true \
    BROWSER=chromium

# Default command — can be overridden at runtime
CMD ["pytest", "--browser", "chromium", "--alluredir=allure-results", "-v", "--tb=short"]
