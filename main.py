import librosa

from midi_creator.midi_creator import MidiCreator
from plotter.plotter import Plotter
from sound_processor.sound_processor import SoundProcessor
from syllable_reader.syllable_reader import SyllableReader
from ultrastar_map_generator.ultrastar_map_generator import UltrastarMapGenerator

audio_filename = 'files/katyusha.mp3'
syllables_filename = 'files/katyusha_lyrics.txt'
output_filename = 'song.txt'
output_midi_filename = 'midi'
title = 'Top'
artist = 'Kek'
mp3 = 'audio.mp3'
min_beat_number = 1

hop_length = 8192
n_fft = 65536
win_length = int(n_fft)
sr = 22050
frame_duration = 0.15  # seconds
y, sr = librosa.load(audio_filename, sr=sr)

# bpm = int(round(SoundProcessor.get_bpm(y, sr)))
bpm = 130.5
track_duration = SoundProcessor.get_duration(y, sr)
# fft_frequencies = SoundProcessor.generate_fft_frequencies(sr, n_fft)
# decibel_matrix = SoundProcessor.detect_pitch_stft(y, n_fft, win_length, hop_length)
# pitches, magnitudes = SoundProcessor.detect_pitch_piptrack(y, sr, n_fft, hop_length, win_length)
extracted_frequencies_autocorrelate = SoundProcessor.detect_pitch_autocorrelate(y, sr, frame_duration)
Plotter.simple_plot(extracted_frequencies_autocorrelate, 'autocorrelate_diagram.png')
# frames_number = SoundProcessor.get_frames_number(decibel_matrix)
# frames_number = SoundProcessor.get_frames_number(pitches)
# extracted_frequencies_piptrack, extracted_frequencies_decibel_matrix = SoundProcessor.extract_frequencies_piptrack(frames_number, pitches, magnitudes)
# frame_duration = SoundProcessor.get_frame_duration(track_duration, frames_number)
beats_frame_duration = SoundProcessor.seconds_to_beats(bpm, frame_duration)
# extracted_frequencies, extracted_frequencies_decibel_matrix = SoundProcessor.extract_frequencies(frames_number, decibel_matrix, fft_frequencies)
# extracted_midis = SoundProcessor.hz_to_midi(extracted_frequencies_piptrack)
extracted_midis = SoundProcessor.hz_to_midi(extracted_frequencies_autocorrelate)
# Plotter.spectrogram_plot(decibel_matrix, y, sr, hop_length, 'track_spectrogram.png')
# Plotter.spectrogram_plot(extracted_frequencies_decibel_matrix, y, sr, hop_length, 'extracted_frequencies_spectrogram.png')
# Plotter.simple_plot(pitches, 'pitches.png')
# Plotter.simple_plot(magnitudes, 'magnitudes.png')
#
notes_with_duration = UltrastarMapGenerator.get_duration_with_note(extracted_midis, beats_frame_duration)
notes_with_duration, gap_in_beats = UltrastarMapGenerator.get_gap(notes_with_duration)
gap = SoundProcessor.seconds_to_ms(SoundProcessor.beats_to_seconds(bpm, gap_in_beats))
# filtered_notes_with_duration = SoundProcessor.filter_computational_errors(notes_with_duration, min_beat_number)
notes_with_rounded_duration = UltrastarMapGenerator.round_beats(notes_with_duration)
notes_with_duration_beat_and_beat_numbers = UltrastarMapGenerator.get_beat_numbers(notes_with_rounded_duration)

# MidiCreator.create_midi(notes_with_duration_beat_and_beat_numbers, bpm, frame_duration, output_midi_filename)

ultrastar_notes_with_duration_beat_and_beat_numbers = UltrastarMapGenerator.midi_to_ultrastar_note(notes_with_duration_beat_and_beat_numbers)
syllables = SyllableReader.get_syllables_from_file(syllables_filename)
notes_with_duration_beat_numbers_and_syllables = UltrastarMapGenerator\
    .get_notes_with_duration_and_syllables(ultrastar_notes_with_duration_beat_and_beat_numbers, syllables)

headers = UltrastarMapGenerator.create_headers(artist, title, str(bpm), str(gap), mp3)
map_lines = UltrastarMapGenerator.generate_map_lines(notes_with_duration_beat_numbers_and_syllables)
lines = headers + map_lines

# Plotter.spectrogram_plot(decibel_matrix, y, sr, hop_length, 'spectrogram.png')

UltrastarMapGenerator.write_list_to_file(output_filename, lines)
