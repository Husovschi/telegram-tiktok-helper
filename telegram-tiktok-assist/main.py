import os
import sys
import time
import re
import requests
import logging
import json

from telethon import TelegramClient, events

logging.basicConfig(level=logging.WARNING)

headers = {
    'user-agent': 'PostmanRuntime/7.29.2',
    'Connection': 'keep-alive'
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

def get_id(url=str) -> str:
    r = requests.get(url, headers=headers)
    return re.findall(r'\d{19}', r.url)[0]

def download_video(id=str):
    api_url = f'https://api19-core-useast5.us.tiktokv.com/aweme/v1/feed/?aweme_id={id}&version_code=262&app_name=musical_ly&channel=App&device_id=null&os_version=14.4.2&device_platform=iphone&device_type=iPhone9'
    r = requests.get(api_url).content.decode('utf8')

    video_url = json.loads(r)['aweme_list'][0]['video']['play_addr']['url_list'][1]
    r = requests.get(video_url)

    with open(f'{id}.mp4', 'wb') as f:
        f.write(r.content)

@events.register(events.NewMessage)
async def handler(event):
    print(event.raw_text)
    if event.out:
        url = re.search(
            r"\bhttps?://(?:m|www|vm)\.tiktok\.com/\S*?\b(?:(?:(?:usr|v|embed|user|video)/|\?shareId=|&item_id=)(\d+)|(?=\w{7})(\w*?[A-Z\d]\w*)(?=\s|\/$))\b",
            event.raw_text)
        if url:
            print('url', url)
            chat = event.chat
            await client.delete_messages(event.chat_id, event.id)
            id = get_id(url.string)
            print(id)
            download_video(id)
            await client.send_file(chat, f'{id}.mp4', video_note=True)
            os.remove(f'{id}.mp4')


client = TelegramClient(
    os.environ.get('TG_SESSION', 'replier'),
    get_env('TG_API_ID', 'Enter your API ID: ', int),
    get_env('TG_API_HASH', 'Enter your API hash: ')
)

with client:
    # This remembers the events.NewMessage we registered before
    client.add_event_handler(handler)

    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
