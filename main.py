import librosa
from enums.enums import GlobalVariables
from input_manager.input_manager import InputManager
from midi_creator.midi_creator import MidiCreator
from sound_processor.sound_processor import SoundProcessor
from syllable_reader.syllable_reader import SyllableReader
from ultrastar_map_generator.ultrastar_map_generator import UltrastarMapGenerator

audio_filename = InputManager.get_audio_file_path()
syllables_filename = InputManager.get_lyrics_file_path()
title = InputManager.get_title()
artist = InputManager.get_artist()
bpm = InputManager.get_bpm()

mp3 = 'audio.mp3'
output_filename = 'song.txt'
output_midi_filename = 'midi'

sr = 22050
frame_duration = 0.1  # seconds
y, sr = librosa.load(audio_filename, sr=sr)
silence_intervals = librosa.effects.split(y=y, frame_length=200, top_db=GlobalVariables.MIN_DB.value)
y = SoundProcessor.erase_silence(y, silence_intervals)

if not bpm:
    bpm = int(round(SoundProcessor.get_bpm(y, sr)))

min_beat_number = SoundProcessor.seconds_to_beats(0.2, bpm)
track_duration = SoundProcessor.get_duration(y, sr)
extracted_frequencies_autocorrelate = SoundProcessor.detect_pitch_autocorrelate(y, sr, frame_duration)

beats_frame_duration = SoundProcessor.seconds_to_beats(bpm, frame_duration)
extracted_midis = SoundProcessor.hz_to_midi(extracted_frequencies_autocorrelate)
notes_with_duration = UltrastarMapGenerator.get_duration_with_note(extracted_midis, beats_frame_duration)
notes_with_duration, gap_in_beats = UltrastarMapGenerator.get_gap(notes_with_duration)
gap = SoundProcessor.seconds_to_ms(SoundProcessor.beats_to_seconds(bpm, gap_in_beats))
filtered_notes_with_duration = SoundProcessor.filter_computational_errors(notes_with_duration, min_beat_number)
notes_with_rounded_duration = UltrastarMapGenerator.round_beats(filtered_notes_with_duration)
notes_with_duration_beat_and_beat_numbers = UltrastarMapGenerator.get_beat_numbers(notes_with_rounded_duration)

MidiCreator.create_midi(notes_with_duration_beat_and_beat_numbers, bpm, output_midi_filename)

ultrastar_notes_with_duration_beat_and_beat_numbers = UltrastarMapGenerator.midi_to_ultrastar_note(notes_with_duration_beat_and_beat_numbers)
syllables = SyllableReader.get_syllables_from_file(syllables_filename)
notes_with_duration_beat_numbers_and_syllables = UltrastarMapGenerator\
    .get_notes_with_duration_and_syllables(ultrastar_notes_with_duration_beat_and_beat_numbers, syllables)

headers = UltrastarMapGenerator.create_headers(artist, title, str(bpm), str(gap), mp3)
map_lines = UltrastarMapGenerator.generate_map_lines(notes_with_duration_beat_numbers_and_syllables)
lines = headers + map_lines

UltrastarMapGenerator.write_list_to_file(output_filename, lines)
