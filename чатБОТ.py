import telebot
import random
import json
from telebot import types

bot = telebot.TeleBot("8717776406:AAEbNW9ABxlsDvJdqPDzimU14EZPX6qhOAU")

# загрузка JSON
with open("books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

user_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    genres = list(books.keys())

    for i in range(0, len(genres), 2):
        if i + 1 < len(genres):
            markup.row(genres[i], genres[i + 1])
        else:
            markup.row(genres[i])

    bot.send_message(message.chat.id, "Выбери жанр:", reply_markup=markup)
    user_state[message.chat.id] = {}

def show_book_menu(user_id, book):
    user_state[user_id]["book"] = book

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Описание", "Оценка")
    markup.row("Другая книга", "Назад")

    text = f'{book["author"]} - {book["title"]}'
    bot.send_message(user_id, text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handler(message):
    user_id = message.chat.id
    text = message.text

    if text == "Назад":
        start(message)
        return

    if text in books:
        user_state[user_id] = {"genre": text}

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Случайная книга", "Все книги")
        markup.row("Назад")

        bot.send_message(user_id, "Выбери действие:", reply_markup=markup)
        return

    if text == "Случайная книга":
        genre = user_state[user_id].get("genre")
        if genre:
            book = random.choice(books[genre])
            show_book_menu(user_id, book)
        return

    if text == "Все книги":
        genre = user_state[user_id].get("genre")

        if genre:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            for b in books[genre]:
                markup.row(b["title"])

            markup.row("Назад")

            user_state[user_id]["mode"] = "choose_book"
