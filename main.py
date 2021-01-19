import librosa
from plotter.plotter import Plotter
from sound_processor.sound_processor import SoundProcessor
from syllable_reader.syllable_reader import SyllableReader
from ultrastar_map_generator.ultrastar_map_generator import UltrastarMapGenerator

audio_filename = 'files/-C-E.mp3'
syllables_filename = 'files/C-E_lyrics.txt'
output_filename = 'katyusha_us.txt'
title = 'Top'
artist = 'Kek'
mp3 = audio_filename
gap = 0
min_beat_number = 2

hop_length = 2048
n_fft = 32768
sr = 22050

y, sr = librosa.load(audio_filename, sr=sr)

bpm = SoundProcessor.get_bpm(y, sr)
track_duration = SoundProcessor.get_duration(y, sr)
fft_frequencies = SoundProcessor.generate_fft_frequencies(sr, n_fft)
decibel_matrix = SoundProcessor.detect_pitch_stft(y, n_fft, hop_length)
frames_number = SoundProcessor.get_frames_number(decibel_matrix)
frame_duration = SoundProcessor.get_frame_duration(track_duration, frames_number)
beats_frame_duration = SoundProcessor.seconds_to_beats(frame_duration, bpm)
extracted_frequencies = SoundProcessor.extract_frequencies(frames_number, decibel_matrix, fft_frequencies)
extracted_midis = SoundProcessor.hz_to_midi(extracted_frequencies)

syllables = SyllableReader.get_syllables_from_file(syllables_filename)
notes_with_duration = UltrastarMapGenerator.get_duration_with_note(extracted_midis, beats_frame_duration)
# filtered_notes_with_duration = SoundProcessor.filter_computational_errors(notes_with_duration, min_beat_number)
notes_with_rounded_duration = UltrastarMapGenerator.round_beats(notes_with_duration)
notes_with_duration_beat_and_beat_numbers = UltrastarMapGenerator.get_beat_numbers(notes_with_rounded_duration)
notes_with_duration_beat_numbers_and_syllables = UltrastarMapGenerator\
    .get_notes_with_duration_and_syllables(notes_with_duration_beat_and_beat_numbers, syllables)

headers = UltrastarMapGenerator.create_headers(artist, title, str(bpm), str(gap), mp3)
map_lines = UltrastarMapGenerator.generate_map_lines(notes_with_duration_beat_numbers_and_syllables)
lines = headers + map_lines

Plotter.spectrogram_plot(decibel_matrix, y, sr, hop_length, 'spectrogram.png')

UltrastarMapGenerator.write_list_to_file(output_filename, lines)
