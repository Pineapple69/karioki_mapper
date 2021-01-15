from enum import Enum


class NoteType(Enum):
    GOLDEN_NOTE = 0
    STANDARD_NOTE = 1
    FREESTYLE_NOTE = 2
    LINE_BREAK = 3
    END_OF_THE_FILE = 4

    @staticmethod
    def get_note_type_string(note_type):
        return {
            NoteType.GOLDEN_NOTE: '*',
            NoteType.STANDARD_NOTE: ':',
            NoteType.FREESTYLE_NOTE: 'F',
            NoteType.LINE_BREAK: '-',
            NoteType.END_OF_THE_FILE: 'E'
        }[note_type]
