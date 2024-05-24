# Telegram-TikTok Video Downloader

This Telegram bot automatically detects TikTok URLs sent in messages and replies with the corresponding downloaded video. It uses Python, Telethon, and yt-dlp to handle interactions and video downloading.

## Features

- **URL Detection**: Automatically detects TikTok URLs in messages.
- **Video Downloading**: Downloads TikTok videos using yt-dlp.
- **Auto-Response**: Replies with the downloaded video directly in the conversation.
- **Cleanup**: Automatically deletes the downloaded videos from the server after sending to conserve disk space.

## Prerequisites

Before you start, ensure you have the following:
- Python 3.8 or higher
- pip (Python package installer)
- Telegram API keys (API ID, API Hash, and Bot Token)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/telegram-tiktok-downloader.git
   cd telegram-tiktok-downloader
   ```

2. **Set up a Python virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r app/requirements.txt
   ```

4. **Environment Variables**

   Create a `.env` file in the root directory and fill in your Telegram credentials:

   ```plaintext
   TG_API_ID=your_telegram_api_id_here
   TG_API_HASH=your_telegram_api_hash_here
   ```

## Usage

To run the bot, execute:

```bash
python app/main.py
```

The bot will start listening for messages containing TikTok URLs and will respond with the video.

## Docker Support

To deploy using Docker, follow these steps:

1. **Build the Docker image**

   ```bash
   docker-compose build
   ```

2. **Start the container**

   ```bash
   docker-compose up
   ```

This will start the bot within a Docker container using the configuration specified in `docker-compose.yml`.