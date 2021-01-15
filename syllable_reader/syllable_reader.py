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
        return syllables
