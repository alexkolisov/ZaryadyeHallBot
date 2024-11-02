import json
from bs4 import BeautifulSoup
import requests
from parser_helpers import *
import re
import time
from zaryadye_bot import bot, get_users
from config import *

def parse_events(max_pages=None):
    print("Start parsing")
    page = 1
    events = []
    urls = []
    is_parsing = True

    while is_parsing:
        print("Looking at page", page)
        url = f'https://zaryadyehall.ru/event/?PAGEN_1={page}'
        answer = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(answer.text, "html.parser")
        names = soup.find_all('a', {'class': 'zh-c-item__name'})

        for name in names:
            if name.attrs.get('href') not in urls:
                events.append(extract_event_info(name.attrs.get('href')))
                urls.append(name.attrs.get('href'))
            else:
                is_parsing = False
                break
        if max_pages and max_pages == page:
            break
        page += 1
    print("Done parsing")
    return events


def get_saved_events():
    try:
        with open('events.json', 'r') as file:
            return json.loads(file.read())
    except:
        return []

def save_events(events):
    with open('events.json', 'w') as file:
        file.write(json.dumps(events, ensure_ascii=False))

def notify_users(new_events):
    for user in get_users():
        for event in new_events:
            url = 'https://zaryadyehall.ru' + event['url']
            text = f"🎭 [{event['название']}]({url})"

            if event.get('программа'):
                text += f"\n\n{event.get('программа')}"
            bot.send_message(user, text, parse_mode="markdown")



def parse():
    old_events = get_saved_events()
    current_events = parse_events(MAX_PAGES)

    changed_events = [event for event in current_events if event not in old_events]
    saved_events = [event for event in current_events if event in old_events]

    print("changed events: ", len(changed_events))
    print("old events: ", len(saved_events))

    notify_users(changed_events)
    save_events(changed_events + saved_events)

while True:
    parse()
    time.sleep(3600)




