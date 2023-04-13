import os
import sys
import time
import re
import requests
import logging
import json

from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeVideo

logging.basicConfig(level=logging.INFO)

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}


def get_long_video_id(url) -> str:
    """Retrieves the video ID from a TikTok URL.

    The function makes a get call to the URL and returns the long ID (19 digits).

    :param url: Video URL
    :return: Long Video ID
    """
    r = requests.get(url, headers=headers, allow_redirects=False)
    if r.status_code == 301:
        return re.findall(r'\d{19}', r.text)[0]
    else:
        return re.findall(r'\d{19}', r.url)[0]


def get_video_url(video_id) -> str:
    """Gets video URL TikTok based on its video ID.

    Returns video URL TikTok.

    :param video_id: long video id.
    :return: Video URL.
    """
    logging.info(f'Getting video URL')
    api_url = f'https://api16-core.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}&version_code=262&app_name=musical_ly&channel=App&device_id=null&os_version=14.4.2&device_platform=iphone&device_type=iPhone9'
    r = requests.get(api_url).content.decode('utf8')

    return json.loads(r)['aweme_list'][0]['video']['play_addr']['url_list'][1]


@events.register(events.NewMessage)
async def handler(event):
    """Telegram client handler.
    """
    if event.out:
        logging.info(f'New message {event.raw_text}')
        url = re.search(
            r"\bhttps?://(?:m|www|vm)\.tiktok\.com/\S*?\b(?:(?:(?:usr|v|embed|user|video)/|\?shareId=|&item_id=)(\d+)|(?=\w{7})(\w*?[A-Z\d]\w*)(?=\s|\/$))\b",
            event.raw_text)
        if url:
            logging.info(f'TikTok link found: {url.string}')
            await client.delete_messages(event.chat_id, event.id)
            video_id = get_long_video_id(url.string)
            logging.info(f'TikTok video ID: {video_id}')
            video_url = get_video_url(video_id)
            logging.info('Sending video to telegram')
            async with client.action(event.chat, 'document') as action:
                await client.send_file(
                    event.chat,
                    video_url,
                    video_note=True,
                    attributes=(DocumentAttributeVideo(0, 0, 0),),
                    progress_callback=action.progress,
                    allow_cache=False
                )


client = TelegramClient(
    os.environ.get('TG_SESSION', 'replier'),
    os.environ.get('TG_API_ID'),
    os.environ.get('TG_API_HASH')
)

with client:
    client.add_event_handler(handler)

    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
