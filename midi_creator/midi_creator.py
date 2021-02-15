from math import inf

from midiutil import MIDIFile

from enums.enums import GlobalVariables


class MidiCreator:

    @staticmethod
    def create_midi(beat_duration_notes_list, bpm, output_filename):
        track = 0
        channel = 0
        time = 0
        volume = 100
        midi = MIDIFile(1)
        midi.addTempo(track, time, bpm)
        for i, beat_duration_note in enumerate(beat_duration_notes_list):
            current_beat = beat_duration_note[0] / GlobalVariables.DURATION_MULTIPLIER.value
            duration = beat_duration_note[1] / GlobalVariables.DURATION_MULTIPLIER.value
            pitch = beat_duration_note[2]
            if pitch != -inf:
                midi.addNote(track, channel, int(pitch), current_beat, duration, volume)

        with open(output_filename + ".mid", "wb") as output_file:
            midi.writeFile(output_file)
