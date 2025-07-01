FROM python:3.11-slim

# Instalacija sistemskih paketa potrebnih za Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Instaliraj aplikaciju
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Instalacija Playwright browsera (headless Chromium)
RUN playwright install --with-deps

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
