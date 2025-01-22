from NotePackage import NotePackage
from Note import Note
from datetime import datetime as dt
from DB_Connection import *
import mysql.connector


def get_input() -> str:
    state: bool = True
    note: str = ""
    buffer: str
    while state:
        buffer = input()
        if buffer == "/end":
            state = False
        else:
            note += f"{buffer}\n"
    return note


def new_note() -> NotePackage:
    note_name = input("Enter Note Name: ")
    note_time =  dt.datetime.now().strftime('%Y-%m-%d')
    description = input("Do you wann add description? (y/n): ")
    if description.lower() == "y":
        description = input("Enter Description: ")
    else:
        description = None
    state: bool = True
    print("Start please")
    note = get_input()
    package = NotePackage()
    package.upd(name= note_name,
                creation_date=note_time,
                last_modification_date=note_time,
                description=description,
                note=Note(note=note))
    return package

def save_note(note: NotePackage) -> None:
    if note == NotePackage():
        return
    try:
        with my_sql.cursor() as my_sql_cursor:
            sql_script = r"INSERT INTO Notes (note_name, creation_date, last_alter_date, description, note) VALUES (%s, %s, %s, %s, %s)"
            data = note.unpack()
            my_sql_cursor.execute(sql_script, data)
            my_sql.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def show_notes() -> None:
    global notes
    notes = load_notes()
    for idx, note in enumerate(notes):
        print(f"{idx + 1} {note.name}")


def edit_note() -> None:
    global notes
    while True:
        show_notes()
        print(f"{len(notes) + 1} exit")
        note_num = input("Enter Note Number: ")
        while not (note_num.isdigit() and  (1 <= int(note_num) <= len(notes) + 1)):
            note_num = input("Please enter a valid Note Number: ")
        if int(note_num) == len(notes) + 1:
            return
        current_note: NotePackage = notes[int(note_num) - 1]
        edit_state : bool = True
        while edit_state:
            edit_options()
            case: str = input("Chose option: ")
            if case == "1":
                delete_note(notes, current_note)
                break
            elif case == "2":
                notes = duplicate_note(notes, current_note)
                pass
            elif case == "3":
                #todo edit curren note
                pass
            elif case == "4":
                break


def edit_options():
    options: list[str] = ["Delete", "Duplicate", "Edit", "Back to notes"]
    print("Chose Options:")
    for option in range(len(options)):
        print(f"N{option + 1} {options[option]}")


def show_options():
    options = ["New note", "Save notes", "Show notes", "Edit note", "Exit"]
    print("Chose Options:")
    for option in range(len(options)):
        print(f"N{option + 1} {options[option]}")


use_state: bool = True
current_note: NotePackage = NotePackage()
notes = []
while use_state:
    show_options()
    option = input()
    if option == "1":
        current_note = new_note()
    elif option == "2":
        save_note(current_note)
    elif option == "3":
        show_notes()
    elif option == "4":
        edit_note()
    elif option == "5":
        exit()
