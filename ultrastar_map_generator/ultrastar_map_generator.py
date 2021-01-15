from copy import copy

from enums.enums import NoteType


class UltrastarMapGenerator:

    @staticmethod
    def create_headers(artist, title, bpm, gap, mp3):
        return [
            '#TITLE: ' + title,
            '#ARTIST: ' + artist,
            '#MP3: ' + mp3,
            '#BPM: ' + bpm,
            '#GAP: ' + gap,
        ]

    @staticmethod
    def create_line(note_type, beat_number, time_before_next_syllable, pitch, syllable):
        return NoteType.get_note_type_string(note_type) + ' ' + \
               beat_number + ' ' + \
               time_before_next_syllable + ' ' + \
               pitch + ' ' + \
               syllable

    @staticmethod
    def create_line_break():
        return NoteType.get_note_type_string(NoteType.LINE_BREAK)

    @staticmethod
    def end_of_the_file():
        return NoteType.get_note_type_string(NoteType.END_OF_THE_FILE)

    @staticmethod
    def generate_map_lines(notes_with_duration_and_syllables):
        lines = []
        for note in notes_with_duration_and_syllables:
            lines.append(
                UltrastarMapGenerator.create_line(NoteType.STANDARD_NOTE, str(note[0]), str(note[1]), str(note[2]),
                                                  note[3]))
        lines.append(UltrastarMapGenerator.end_of_the_file())
        return lines

    @staticmethod
    def get_map_lines(extracted_midis, duration):
        lines = []
        # beat number, duration, note
        line = [0, duration, extracted_midis[0]]
        previous_line_index = 0
        for midi_index in range(1, len(extracted_midis) - 1):
            midi_note = extracted_midis[midi_index]
            if midi_note == line[2]:
                line[1] += duration
            else:
                lines.append(copy(line))
                line[0] = lines[previous_line_index][0] + lines[previous_line_index][1] + 1
                line[1] = duration
                line[2] = midi_note
                previous_line_index += 1
        return lines

    @staticmethod
    def get_notes_with_duration_and_syllables(notes_with_duration, syllables):
        for index, note_with_duration in enumerate(notes_with_duration):
            note_with_duration.append(syllables[index])
        return notes_with_duration

    @staticmethod
    def write_list_to_file(file_name, elements):
        with open(file_name, 'a') as file:
            for element in elements:
                file.write(element + '\n')
            file.close()
