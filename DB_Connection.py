from NotePackage import NotePackage
import datetime as dt
import mysql.connector

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

def load_notes() -> None:
    notes = []
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
    return notes

def delete_note(notes, note: NotePackage) -> None:
    for i in notes:
        if i.name == note.name:
            notes.remove(i)
    my_sql_cursor = my_sql.cursor()
    delete_script = r"DELETE FROM Notes WHERE note_name=%s"
    values = (note.name,)
    my_sql_cursor.execute(delete_script, values)
    my_sql.commit()

def duplicate_note(notes, note: NotePackage) -> None:
    duplicate_note = NotePackage(name=f"{note.name}_Duplicate",
                                 description=note.description,
                                 note=note.note,
                                 creation_date=note.creation_date,
                                 last_modification_date=dt.datetime.now().strftime('%Y-%m-%d'))
    notes.append(duplicate_note)
    save_note(duplicate_note)
    return notes

def join_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="my_laptop_user",
        password="pass_to_db",
        database="NotesDB"
    )
    return mydb


my_sql = join_db()