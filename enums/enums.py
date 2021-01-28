from enum import Enum


class GlobalVariables(Enum):
    HIGHEST_NOTE = 1046.5  # C6 highest note sung by a soprano
    LOWEST_NOTE = 65.406  # C2 lowest note sung by a bass
    MAGIC_CONSTANT = 60000000  # took from BPM = 60,000,000/tempo it's used to calculate bpm based on midi tempo
    TICKS_PER_QUARTER_NOTE = 192
    DURATION_MULTIPLIER = 4


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
