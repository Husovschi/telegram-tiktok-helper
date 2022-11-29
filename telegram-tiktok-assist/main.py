import os
import sys
import time
import re
import requests
import logging
import json

from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO)

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)

def get_video_id(url) -> str:
    r = requests.get(url, headers=headers, allow_redirects=False)
    if r.status_code == 301:
        return re.findall(r'\d{19}', r.text)[0]
    else:
        return re.findall(r'\d{19}', r.url)[0]

def download_video(id) -> None:
    logging.info(f'Downloading video')
    api_url = f'https://api19-core-useast5.us.tiktokv.com/aweme/v1/feed/?aweme_id={id}&version_code=262&app_name=musical_ly&channel=App&device_id=null&os_version=14.4.2&device_platform=iphone&device_type=iPhone9'
    r = requests.get(api_url).content.decode('utf8')

    video_url = json.loads(r)['aweme_list'][0]['video']['play_addr']['url_list'][1]
    r = requests.get(video_url)

    with open(f'{id}.mp4', 'wb') as f:
        f.write(r.content)


@events.register(events.NewMessage)
async def handler(event):
    if event.out:
        logging.info(f'New message {event.raw_text}')
        url = re.search(
            r"\bhttps?://(?:m|www|vm)\.tiktok\.com/\S*?\b(?:(?:(?:usr|v|embed|user|video)/|\?shareId=|&item_id=)(\d+)|(?=\w{7})(\w*?[A-Z\d]\w*)(?=\s|\/$))\b",
            event.raw_text)
        if url:
            logging.info(f'TikTok link found: {url.string}')
            await client.delete_messages(event.chat_id, event.id)
            video_id = get_video_id(url.string)
            logging.info(f'TikTok video ID: {video_id}')
            download_video(video_id)
            logging.info('Sending video to telegram')
            await client.send_file(event.chat, f'{video_id}.mp4', video_note=True)
            os.remove(f'{video_id}.mp4')

client = TelegramClient(
    os.environ.get('TG_SESSION', 'replier'),
    get_env('TG_API_ID', 'Enter your API ID: '),
    get_env('TG_API_HASH', 'Enter your API hash: ')
)

with client:
    client.add_event_handler(handler)

    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
