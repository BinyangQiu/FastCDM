# Use a slim Python base image for smaller size and faster builds
FROM python:3.10-slim

# Set environment variables to optimize Python execution and set up user paths
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Create a non-root user 'user' with UID 1000 (required for Hugging Face Spaces)
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR $HOME/app

# Install system dependencies
# Combined into a single RUN instruction to reduce image layers
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    # Chrome dependencies
    libx11-6 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    fonts-liberation \
    xdg-utils \
    libxkbcommon0 \
    # OpenCV dependencies
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (Version 20.x)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome (Version 135.0.7049.52)
# Using chrome-for-testing public archive
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.52/linux64/chrome-linux64.zip \
    && unzip -q chrome-linux64.zip \
    && mv chrome-linux64 /opt/chrome \
    && ln -s /opt/chrome/chrome /usr/local/bin/google-chrome \
    && rm chrome-linux64.zip

# Install Python dependencies
# We install heavy dependencies first to leverage Docker layer caching
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    numpy>=1.20 \
    opencv-python-headless>=4.5 \
    selenium>=4 \
    webdriver-manager>=4 \
    scikit-image \
    gradio

# Copy the application code
COPY --chown=user . $HOME/app

# Install Chromedriver (Version 135.0.7049.114)
# Installing into 'driver/chromedriver' as expected by scripts/app.py and README
RUN mkdir -p driver \
    && wget -q https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.114/linux64/chromedriver-linux64.zip \
    && unzip -q chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver driver/ \
    && chmod +x driver/chromedriver \
    && rm -r chromedriver-linux64 chromedriver-linux64.zip \
    && chown -R user:user driver

# Install the fastcdm package
RUN pip install --no-cache-dir .

# Switch to the non-root user
USER user

# Expose port 7860 for Hugging Face Spaces / Gradio
EXPOSE 7860

# Start the application
CMD ["python3", "scripts/app.py"]
