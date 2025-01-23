from DB_Connection import save_note, load_notes
from NotePackage import NotePackage
import telebot as tb
import datetime as dt
import json

with open('config.json') as file:
    config = json.load(file)


API = config["bot_token"]
bot = tb.TeleBot(API)


user_state:dict = {}
note_template: NotePackage = NotePackage()
notes = []


def show_menu(chat_id: int) -> None:
    menu_text = ("Виберіть опцію:\n"
                 "/menu - повернення до головного меню\n"
                 "/new - Нова нотатка\n"
                 "/show - Показати минулі нотатки\n"
                 )
    bot.send_message(chat_id, menu_text)

def note_info(note: NotePackage) -> str:
    text = (f"Note name: {note.name}\n"
            f"Creation date: {note.creation_date}\n"
            f"Description: {note.description}\n"
            f"Note: \n{note.note.note}")
    return text

@bot.message_handler(commands=['start'])
def echo(message):
    bot.send_message(message.chat.id, text="/New\n /Show")
    user_state[message.chat.id] = "menu"

@bot.message_handler(commands=['new', "New"])
def echo(message):
    user_state[message.chat.id] = "new"
    bot.send_message(message.chat.id, text="Enter note name")

@bot.message_handler(commands=["end"])
def echo(message):
    user_state[message.chat.id] = "menu"


@bot.message_handler(commands=["show"])
def echo(message):
    global notes
    notes = load_notes()
    text = ''.join(f"{idx + 1} {note.name}\n" for idx, note in enumerate(notes))
    bot.send_message(message.chat.id, text=str(text))
    bot.send_message(message.chat.id, "Enter Note Number: ")
    user_state[message.chat.id] = "show"

@bot.message_handler(func=lambda message: user_state[message.chat.id] == "new")
def echo(message):
    note_template.upd(name=message.text,
                      creation_date=dt.datetime.now().strftime('%Y-%m-%d'),
                      last_modification_date=dt.datetime.now().strftime('%Y-%m-%d'))
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
    bot.send_message(message.chat.id, text="Note successfully created")
    save_note(note_template)
    user_state[message.chat.id] = "menu"

@bot.message_handler(func=lambda message: user_state[message.chat.id] == "show")
def echo(message):
    while not (message.text.isdigit() and (1 <= int(message.text) <= len(notes))):
        bot.reply_to(message, "Please enter a valid Note Number: ")
        return
    bot.send_message(message.chat.id, text=note_info(notes[int(message.text)-1]))

@bot.message_handler(func=lambda message: user_state[message.chat.id] == "menu")
def echo(message):
    show_menu(message.chat.id)


bot.polling()