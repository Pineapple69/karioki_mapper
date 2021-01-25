from math import inf

from midiutil import MIDIFile


class MidiCreator:

    @staticmethod
    def create_midi(beat_duration_notes_list, bpm, ms_per_tick, output_filename):
        track = 0
        channel = 0
        time = 0
        volume = 100
        ticks_per_quarter_note = int(MidiCreator.get_ticks_per_quarter_note(bpm, ms_per_tick))
        midi = MIDIFile(1, eventtime_is_ticks=True, ticks_per_quarternote=ticks_per_quarter_note)
        midi.addTempo(track, time, bpm)

        for i, beat_duration_note in enumerate(beat_duration_notes_list):
            beat = beat_duration_note[0]
            duration = beat_duration_note[1]
            pitch = beat_duration_note[2]
            if pitch != -inf:
                midi.addNote(track, channel, int(pitch), beat, duration, volume)

        with open(output_filename + ".mid", "wb") as output_file:
            midi.writeFile(output_file)

    @staticmethod
    def get_ticks_per_quarter_note(bpm, ms_per_tick):
        return 60000 / (bpm * ms_per_tick)
