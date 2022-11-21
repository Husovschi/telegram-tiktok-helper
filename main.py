#!/usr/bin/env python3

import os
import sys
import time
import re

from telethon import TelegramClient, events
from tiktok_downloader import TiktokDownloader

import logging

logging.basicConfig(level=logging.WARNING)


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
            TiktokDownloader().download_video(url.string)
            await client.send_file(chat, 'out.mp4', video_note=True)
            os.remove('out.mp4')


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
