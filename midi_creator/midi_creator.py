from math import inf

from midiutil import MIDIFile


class MidiCreator:

    @staticmethod
    def create_midi(beat_duration_notes_list, bpm, output_filename):
        track = 0
        channel = 0
        time = 0
        volume = 100
        midi = MIDIFile(1, eventtime_is_ticks=True)
        midi.addTempo(track, time, 20)

        for i, beat_duration_note in enumerate(beat_duration_notes_list):
            beat = beat_duration_note[0]
            duration = beat_duration_note[1]
            pitch = beat_duration_note[2]
            if pitch != -inf:
                midi.addNote(track, channel, int(pitch), beat, duration, volume)

        with open(output_filename + ".mid", "wb") as output_file:
            midi.writeFile(output_file)
