from copy import copy
from math import inf

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
    def create_break_line(beat_number):
        return NoteType.get_note_type_string(NoteType.LINE_BREAK) + ' ' + beat_number

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
            line = ''
            if note[3] == NoteType.LINE_BREAK:
                line = UltrastarMapGenerator.create_break_line(str(note[0]))
            else:
                line = UltrastarMapGenerator.create_line(
                    NoteType.STANDARD_NOTE, str(note[0]), str(note[1]), str(note[2]), note[3]
                )
            lines.append(line)
        lines.append(UltrastarMapGenerator.end_of_the_file())
        return lines

    @staticmethod
    def get_duration_with_note(extracted_midis, duration):
        lines = []
        line = [duration, extracted_midis[0]]
        for midi_index in range(1, len(extracted_midis) - 1):
            midi_note = extracted_midis[midi_index]
            if midi_note == line[1] or UltrastarMapGenerator.is_octave(line[1], midi_note):
                line[0] += duration
            else:
                lines.append(copy(line))
                line[0] = duration
                line[1] = midi_note
        return lines

    @staticmethod
    def get_ultrastar_note(midi_note):
        return midi_note - 60

    @staticmethod
    def is_octave(note_a, note_b):
        return note_a - 12 == note_b

    @staticmethod
    def get_beat_numbers(duration_with_notes):
        duration_with_notes[0].insert(0, 0)
        for index in range(1, len(duration_with_notes)):
            previous_element = duration_with_notes[index - 1]
            beat_number = previous_element[0] + previous_element[1] + 1
            duration_with_notes[index].insert(0, beat_number)
        return duration_with_notes

    @staticmethod
    def get_notes_with_duration_and_syllables(notes_with_duration, syllables):
        syllables_index = 0
        for index, note_with_duration in enumerate(notes_with_duration):
            syllable = syllables[syllables_index]
            syllables_index += 1
            if note_with_duration[2] == -inf:
                syllable = NoteType.LINE_BREAK
                syllables_index -= 1
            note_with_duration.append(syllable)
        return notes_with_duration

    @staticmethod
    def write_list_to_file(file_name, elements):
        with open(file_name, 'a') as file:
            for element in elements:
                file.write(element + '\n')
            file.close()

    @staticmethod
    def round_beats(us_lines):
        return list(map(lambda us_line: [round(us_line[0]), us_line[1]], us_lines))

    @staticmethod
    def midi_to_ultrastar_note(midi_notes):
        for i, midi_note in enumerate(midi_notes):
            midi_note[-1] = UltrastarMapGenerator.get_ultrastar_note(midi_note[-1])
        return midi_notes
