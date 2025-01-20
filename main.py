

def main():
    from NotePackage import NotePackage
    from datetime import datetime as dt
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
        note_time =  dt.now().strftime('%Y-%m-%d')
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
                    note=note)
        return package

    def save_note(note: NotePackage) -> None:
        try:
            with my_sql.cursor() as my_sql_cursor:
                sql_script = r"INSERT INTO Notes (note_name, creation_date, last_alter_date, description, note) VALUES (%s, %s, %s, %s, %s)"
                data = note.unpack()
                my_sql_cursor.execute(sql_script, data)
                my_sql.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def load_notes() -> None:
        notes.clear()
        my_sql_cursor = my_sql.cursor()
        script = r"SELECT * FROM Notes"
        my_sql_cursor.execute(script)
        result = my_sql_cursor.fetchall()
        for row in result:
            temp_note = NotePackage()
            temp_note.upd(name=row[0],
                          creation_date=row[1],
                          last_modification_date=row[2],
                          description=row[3],
                          note=row[4])
            notes.append(temp_note)


    def delete_note(note: NotePackage) -> None:
        for i in notes:
            if i.name == note.name:
                notes.remove(i)
        my_sql_cursor = my_sql.cursor()
        delete_script = r"DELETE FROM Notes wHERE name=%s"
        values = (note.name)
        my_sql_cursor.execute(delete_script, values)
        my_sql.commit()

    def delete_note_shell():
        show_notes()
        note_to_delete = input("Enter Note Number: ")
        while not (note_to_delete.isdigit() and  (1 <= int(note_to_delete) < len(notes))):
            note_to_delete = input("Please enter a valid Note Number: ")
        note_to_delete = int(note_to_delete)
        delete_note(notes[note_to_delete])


    def show_notes() -> None:
        load_notes()
        for idx, note in enumerate(notes):
            print(f"{idx + 1} {note.name}")


    def edit_note() -> None:
        show_notes()
        note_num = input("Enter Note Number: ")
        while not (note_num.isdigit() and  (1 <= int(note_num) <= len(notes))):
            note_num = input("Please enter a valid Note Number: ")
        current_note: NotePackage = notes[int(note_num) - 1]
        edit_state : bool = True
        while edit_state:
            edit_options()
            case: str = input("Chose option: ")
            if case == "1":
                delete_note_shell()
            elif case == "2":
                #TODO Overwrite
                pass
            elif case == "3":
                #todo edit curren note
                pass

    def join_db():
        mydb = mysql.connector.connect(
            host="localhost",
            user="my_laptop_user",
            password="pass_to_db",
            database="NotesDB"
        )
        return mydb


    def edit_options():
        options: list[str] = ["Delete", "Overwrite", "Duplicate", "Edit"]
        print("Chose Options:")
        for option in range(len(options)):
            print(f"N{option + 1} {options[option]}")


    def show_options():
        options = ["New note", "Save notes", "Show notes", "Edit note", "Exit"]
        print("Chose Options:")
        for option in range(len(options)):
            print(f"N{option + 1} {options[option]}")


    use_state: bool = True
    current_note: dict = {}
    my_sql = join_db()
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

if __name__ == '__main__':
    main()