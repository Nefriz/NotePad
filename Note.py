class Note:
    def __init__(self, note):
        self.note = note

    def copy(self):
        return self.note

    def get_line(self, index):
        lines = self.note.split('\n')
        return lines[index]

    def replace(self, line_index, start, end, new_note):
        lines = self.note.split('\n')
        line = lines[line_index].split(" ")
        line[start:end] = [new_note]
        lines[line_index] = " ".join(line)
        self.note = "\n".join(lines)
    def __str__(self):
        return self.note

# Example usage
note = Note("My dog is big")
note.replace(0, 1, 3, "not")
print(note.note)
