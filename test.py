import ast
import re
import requests
import json

headers = {
    'user-agent': 'PostmanRuntime/7.29.2',
    'Connection': 'keep-alive'
}

response = requests.get('https://vm.tiktok.com/ZMFQjGSnc/', headers=headers)

id = re.findall(r'\d{19}', response.url)[0]

url = f'https://api19-core-useast5.us.tiktokv.com/aweme/v1/feed/?aweme_id={id}&version_code=262&app_name=musical_ly&channel=App&device_id=null&os_version=14.4.2&device_platform=iphone&device_type=iPhone9'
print(url)
r = requests.get(url)

nush = r.content.decode('utf8')

with open(f'{id}.json', 'wb') as f:
    f.write(r.content)

jsonlol = json.loads(nush)

r = requests.get(jsonlol['aweme_list'][0]['video']['download_addr']['url_list'][0], allow_redirects=True)
with open(f'{id}.mp4', 'wb') as f:
    f.write(r.content)
