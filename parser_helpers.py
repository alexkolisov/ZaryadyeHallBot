import re
from bs4 import BeautifulSoup
import requests


def get_headers():
    return {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
    }


def clean_string(s):
    symbols = "\n\t\r"

    for symbol in symbols:
        s = s.replace(symbol, " ")

    return re.sub(' +', ' ', s).strip()


def extract_date(soup):
    object = soup.find("div", {'class': 'zh-c-concert__left'}).find("div", {'class': 'zh-h2'})
    if object:
        return clean_string(object.get_text())


def extract_title(soup):
    object = soup.find("h1", {'class': 'zh-c-concert__title'})
    if object:
        return clean_string(object.get_text())


def extract_description(soup):
    object = soup.find("div", {'class': 'zh-c-concert__content'})
    if object:
        return clean_string(object.get_text())


def extract_time(soup):
    object = soup.find("li", {'class': 'zh-meta__item zh-meta-item zh-meta-item_time'})
    if object:
        return clean_string(object.get_text())


def extract_hall(soup):
    object = soup.find("li", {'class': 'zh-meta__item zh-meta-item zh-meta-item_hall'})
    if object:
        return clean_string(object.get_text())


def extract_program(soup):
    object = soup.find("div", {'class': 'zh-accordion__body'})
    if object:
        return clean_string(object.get_text())
    else:
        return 'программа пока неизвестна'


def extract_duration(soup):
    object = soup.find("div", {'class': 'zh-c-concert__value'})
    if object:
        return clean_string(object.get_text())
    return 'продолжительность пока неизвестна'


def extract_event_info(page):
    answer = requests.get(f'https://zaryadyehall.ru' + page, headers=get_headers())
    soup = BeautifulSoup(answer.text, "html.parser")

    description = {
        'url': page,
        'название': extract_title(soup),
        'опиcание': extract_description(soup),
        'дата': extract_date(soup),
        'время': extract_time(soup),
        'зал': extract_hall(soup),
        'продолжительность': extract_duration(soup),
        'программа': extract_program(soup)
    }
    return description
