FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip gnupg curl xvfb libxi6 libgconf-2-4 libappindicator1 libnss3 libxss1 \
    libasound2 fonts-liberation libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    libxcb-dri3-0 libxcomposite1 libxcursor1 libxdamage1 libxrandr2 x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb \
    && apt install -y ./chrome.deb \
    && rm chrome.deb

# Set up ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" \
    | grep -A 10 "\"$CHROME_VERSION\"" | grep "linux64" | grep "chromedriver" | grep -oP 'https://[^"]+') && \
    wget -O chromedriver.zip "$CHROMEDRIVER_VERSION" && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver.zip

# Set environment variables for headless Chrome
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy project files
WORKDIR /app
COPY . /app

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.enableCORS=false"]
