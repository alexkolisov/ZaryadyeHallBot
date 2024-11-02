import json

import telebot
from telebot import types
import requests
from datetime import datetime, timedelta
import random
import telebot
from config import TOKEN

keyboard = types.InlineKeyboardMarkup()
bot = telebot.TeleBot(token=TOKEN)

def get_users():
    try:
        with open('users.json') as file:
            return json.load(file)
    except:
        return []

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)

@bot.message_handler(commands=['subscribe'])
def add_user(message):
    users = get_users()
    user = message.chat.id
    if user not in users:
        users.append(user)
        save_users(users)
        bot.send_message(user, "вы подписались на рассылку")
    else:
        bot.send_message(user, "вы уже  подписаны на рассылку")

@bot.message_handler(commands=['unsubscribe'])
def remove_user(message):
    user = message.chat.id
    users = get_users()
    if user in users:
        users.remove(user)
        save_users(users)
        bot.send_message(user, 'вы отписались от рассылки')
    else:
        bot.send_message(user, 'вы уже отписаны от рассылки')

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)