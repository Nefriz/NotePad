import datetime
from Note import Note
class NotePackage:
    def __init__(self, name: str = None,
                 creation_date: datetime = None,
                 last_modification_date: datetime = None,
                 description: str = None,
                 note: str = None):
        self.name = name
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.description = description
        self.note: Note = Note(note)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "creation_date": self.creation_date,
            "last_modification_date": self.last_modification_date,
            "description": self.description,
            "note": self.note
        }

    def unpack(self):
        return (self.name,
                self.creation_date,
                self.last_modification_date,
                self.description,
                self.note.note)

    def upd(self, name: str = None,
            creation_date: datetime = None,
            last_modification_date: datetime = None,
            description: str = None,
            note: str = None):
        if name is not None:
            self.name = name
        if creation_date is not None:
            self.creation_date = creation_date
        if last_modification_date is not None:
            self.last_modification_date = last_modification_date
        if description is not None:
            self.description = description
        if note is not None:
            self.note = note

    def pack(self):
        return self.to_dict()

    def __str__(self):
        return rf"{self.name}, {self.creation_date}, {self.last_modification_date}, {self.description}, {self.note}"
