import librosa
import matplotlib.pyplot as plt
import numpy as np

from enums.enums import GlobalVariables
from miscellaneous.miscellaneous import Miscellaneous


class SoundProcessor:

    @staticmethod
    def detect_pitch_stft(y, n_fft, win_length, hop_length):
        s_db = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)), ref=np.max)
        return s_db

    @staticmethod
    def detect_pitch_piptrack(y, sr, n_fft, hop_length, win_length):
        return librosa.piptrack(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, win_length=win_length)

    @staticmethod
    def detect_pitch_autocorrelate(y, sr, frame_length):
        pitches = []
        audio_length = len(y)
        chunk_length = int(sr * frame_length)
        for chunk_beg_index in range(0, audio_length, chunk_length):
            chunk_end_index = chunk_beg_index + chunk_length
            if chunk_end_index < audio_length:
                pitches.append(SoundProcessor.autocorrelate(y[chunk_beg_index:chunk_end_index], sr))
            else:
                pitches.append(SoundProcessor.autocorrelate(y[chunk_beg_index:], sr))
        return pitches

    @staticmethod
    def autocorrelate(y, sr):
        r = librosa.autocorrelate(y)
        t_lo = sr / GlobalVariables.HIGHEST_NOTE.value
        t_hi = sr / GlobalVariables.LOWEST_NOTE.value
        r[:int(t_lo)] = 0
        r[int(t_hi):] = 0
        t_max = r.argmax()
        return GlobalVariables.SILENCE.value if t_max == 0 else sr / t_max

    @staticmethod
    def correlate(vec_0, vec_1):
        return np.correlate(vec_0, vec_1)

    @staticmethod
    def extract_frequencies_piptrack(frames_number, pitches, magnitudes):
        decibel_matrix = SoundProcessor.create_decibel_matrix(pitches.shape)
        extracted_frequencies = []
        for frame_number_index in range(frames_number):
            index = magnitudes[:, frame_number_index].argmax()
            pitch = pitches[index, frame_number_index]
            for i in range(-2, 2):
                decibel_matrix[index + i, frame_number_index] = -10
            extracted_frequencies.append(pitch)
        return extracted_frequencies, decibel_matrix


    @staticmethod
    def get_duration(y, sr):
        return librosa.core.get_duration(y=y, sr=sr)

    @staticmethod
    def erase_silence(y, silence_intervals):
        y_without_silence = np.array([0.0] * len(y))
        for interval in silence_intervals:
            y_without_silence[interval[0]:interval[1]] = y[interval[0]:interval[1]]
        return y_without_silence

    @staticmethod
    def generate_fft_frequencies(sr, n_fft):
        return librosa.fft_frequencies(sr, n_fft)

    @staticmethod
    def get_frames_number(decibel_matrix):
        return decibel_matrix.shape[1]

    @staticmethod
    def get_frame_duration(track_duration, frames_number):
        return track_duration / frames_number

    @staticmethod
    def extract_frequencies(frames_number, decibel_matrix, fft_frequencies):
        extracted_frequencies = np.array([0] * frames_number)
        extracted_frequencies_decibel_matrix = np.array([[-80.0000] * frames_number] * decibel_matrix.shape[0])
        for frame_number in range(frames_number):
            frame = decibel_matrix[:, frame_number]
            max_frame_magnitude = frame.max()
            max_frame_magnitude_index = np.where(frame == max_frame_magnitude)[0]
            if max_frame_magnitude > -80:
                frequency = fft_frequencies[max_frame_magnitude_index]
                if GlobalVariables.HIGHEST_NOTE.value >= frequency >= GlobalVariables.LOWEST_NOTE.value:
                    for i in range(-5, 5):
                        extracted_frequencies_decibel_matrix[max_frame_magnitude_index + i, frame_number] = frame[max_frame_magnitude_index]
                    extracted_frequencies[frame_number] = frequency
        return extracted_frequencies, extracted_frequencies_decibel_matrix

    @staticmethod
    def create_decibel_matrix(matrix_shape):
        return np.array([[-80.0000] * matrix_shape[1]] * matrix_shape[0])


    @staticmethod
    def hz_to_midi(extracted_frequencies):
        extracted_midi = librosa.core.hz_to_midi(extracted_frequencies)
        extracted_midi = np.around(extracted_midi)
        return extracted_midi

    @staticmethod
    def get_bpm(y, sr):
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        return tempo

    @staticmethod
    def seconds_to_beats(bpm, seconds):
        return ((bpm * seconds) / 60) * GlobalVariables.DURATION_MULTIPLIER.value

    @staticmethod
    def get_decibel_matrix_column(decibel_matrix, index):
        return decibel_matrix[:, index]

    @staticmethod
    def get_part_of_decibel_matrix(frames_number, decibel_matrix, index):
        part_of_decibel_matrix = np.array([[-80.0000] * frames_number] * decibel_matrix.shape[0])
        part_of_decibel_matrix[:, index] = decibel_matrix[:, index]
        return part_of_decibel_matrix

    @staticmethod
    def get_part_of_waveform(y, beg, end):
        part_of_waveform = np.array([0.0] * len(y))
        part_of_waveform[beg:end] = y[beg:end]
        return part_of_waveform

    @staticmethod
    def beats_to_seconds(bpm, beats):
        return (beats * 60) / (bpm * GlobalVariables.DURATION_MULTIPLIER.value)

    @staticmethod
    def seconds_to_ms(seconds):
        return round(seconds * 1000)

    @staticmethod
    def filter_computational_errors(duration_with_midi_list, min_note_duration):
        def find_next_legal_note(midi_list_pos):
            length = len(duration_with_midi_list)
            if midi_list_pos <= length:
                for index in range(midi_list_pos, length):
                    if duration_with_midi_list[index][0] >= min_note_duration:
                        return index
            return -1

        def sum_range(beg, end, beg_offset=0, add_to_end=False):
            additional_note_length = Miscellaneous.foldr(lambda x, y: x[0] + y, 0, duration_with_midi_list[beg + beg_offset:end])
            index = beg - beg_offset
            if add_to_end:
                index = end
            duration_with_midi_list[index][0] += additional_note_length
            del duration_with_midi_list[beg + beg_offset:end]

        legal_note_index = find_next_legal_note(0)
        next_legal_note_index = 0

        if legal_note_index > 0:
            sum_range(0, legal_note_index, add_to_end=True)
            legal_note_index = 0

        while find_next_legal_note(next_legal_note_index + 1) != -1:
            next_legal_note_index = find_next_legal_note(next_legal_note_index + 1)
            if next_legal_note_index - legal_note_index > 1:
                if duration_with_midi_list[legal_note_index][1] == duration_with_midi_list[next_legal_note_index][1]:
                    sum_range(legal_note_index, next_legal_note_index)
                else:
                    sum_range(legal_note_index, next_legal_note_index, 1)
                    legal_note_index -= 1
                legal_note_index = next_legal_note_index - legal_note_index
                next_legal_note_index = legal_note_index
            else:
                legal_note_index = next_legal_note_index

        if next_legal_note_index != len(duration_with_midi_list) - 1:
            sum_range(next_legal_note_index, len(duration_with_midi_list), 1)

        return duration_with_midi_list

