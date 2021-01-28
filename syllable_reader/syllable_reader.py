from enums.enums import NoteType


class SyllableReader:

    @staticmethod
    def get_syllables_from_file(file_name):
        file = open(file_name, 'r')
        lines = file.readlines()
        syllables = []
        for line in lines:
            line = line.rstrip()
            line = line.replace(',', '')
            syllables += line.split(' ')
            syllables.append(NoteType.LINE_BREAK)
        return syllables
