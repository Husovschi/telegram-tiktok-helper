import os
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeVideo
import tiktok_downloader
from moviepy.editor import VideoFileClip

# Setup the TelegramClient with environment variables
client = TelegramClient(
    os.environ.get('TG_SESSION', 'replier'),
    os.environ.get('TG_API_ID'),
    os.environ.get('TG_API_HASH')
)


@client.on(events.NewMessage(pattern=r'https?://(www\.)?tiktok\.com/\S+'))
async def handler(event):
    # Extract URL and download video
    url = event.message.text
    video_path = tiktok_downloader.download_video(url)

    # Extract video metadata using moviepy
    try:
        with VideoFileClip(video_path) as clip:
            width, height = clip.size
            duration = int(clip.duration)

        # Reply with the downloaded video
        await client.send_file(
            event.chat_id,
            file=video_path,
            supports_streaming=True,
            attributes=[DocumentAttributeVideo(
                duration=duration,
                w=width,
                h=height,
                supports_streaming=True
            )],
            allow_cache=False
        )
    finally:
        # Ensure the video file is deleted after sending or if an error occurs
        if os.path.exists(video_path):
            os.remove(video_path)


def main():
    print("Bot is running...")
    client.start(bot_token=os.environ.get('TG_BOT_TOKEN'))
    client.run_until_disconnected()


if __name__ == '__main__':
    main()
