import telebot as tb
import json
from NotePackage import NotePackage
import datetime as dt
from main import save_note

with open('config.json') as file:
    config = json.load(file)


API = config["bot_token"]
bot = tb.TeleBot(API)


user_state:dict = {}
note_template: NotePackage = NotePackage()
def show_menu(chat_id: int) -> None:
    menu_text = ("Виберіть опцію:\n"
                 "/menu - повернення до головного меню\n"
                 "/new - Нова нотатка\n"
                 "/show - Показати минулі нотатки\n"
                 )
    bot.send_message(chat_id, menu_text)


@bot.message_handler(commands=['start'])
def echo(message):
    bot.send_message(message.chat.id, text="/NewNote\n /ShowNotes")
    user_state[message.chat.id] = "menu"

@bot.message_handler(commands=['new', "NewNote"])
def echo(message):
    user_state[message.chat.id] = "new"
    bot.send_message(message.chat.id, text="Enter note name")

@bot.message_handler(commands=["end"])
def echo(message):
    user_state[message.chat.id] = "menu"


@bot.message_handler(func=lambda message: user_state[message.chat.id] == "new")
def echo(message):
    note_template.upd(name=message.text,
                      creation_date=dt.now().strftime('%Y-%m-%d'),
                      last_modification_date=dt.now().strftime('%Y-%m-%d'))
    user_state[message.chat.id] = "description"
    bot.send_message(message.chat.id, text="Do you wanna add description? /y|/n")

@bot.message_handler(func=lambda message: user_state[message.chat.id] == "description")
def echo(message):
    if message.text == "/y":
        bot.send_message(message.chat.id, text="Enter your description:")
    else:
        if message.text != "/n":
            note_template.upd(description=message.  text)
        user_state[message.chat.id] = "note"
        bot.send_message(message.chat.id, text="Write a note")

@bot.message_handler(func=lambda message: user_state[message.chat.id] == "note")
def echo(message):
    note_template.upd(note=message.text)
    bot.send_message(message.chat.id, text=user_state[message.chat.id])
    save_note(note_template)


@bot.message_handler()
def echo(message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_state[user_id] == "menu":
        show_menu(chat_id)

    elif user_state[user_id] == "new":
        bot.send_message(chat_id, text="Enter Note name")
        print(message.text)


bot.polling()