import librosa
import numpy as np

from enums.enums import GlobalVariables


class SoundProcessor:

    @staticmethod
    def detect_pitch_stft(y, n_fft, win_length, hop_length):
        s_db = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)), ref=np.max)
        return s_db

    @staticmethod
    def detect_pitch_piptrack(y, sr):
        return librosa.piptrack(y=y, sr=sr)

    @staticmethod
    def get_duration(y, sr):
        return librosa.core.get_duration(y=y, sr=sr)

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
        filtered_list = [duration_with_midi_list[0]]
        midi_list_max_index = len(duration_with_midi_list)

        for index in range(1, midi_list_max_index):
            current_note = duration_with_midi_list[index]
            if index <= midi_list_max_index:
                next_note = duration_with_midi_list[index + 1]
                if current_note[0] < min_note_duration:
                    if filtered_list[-1][1] != current_note[1] and filtered_list[-1][1] == next_note[1]:
                        filtered_list[0] += current_note[0]
                else:
                    filtered_list.append(current_note)
            else:
                filtered_list.append(current_note)

        if filtered_list[0][0] < min_note_duration:
            filtered_list[1][0] += filtered_list[0][0]
            del filtered_list[0]

        midi_list_last_item = duration_with_midi_list[midi_list_max_index]
        if midi_list_last_item[0] < min_note_duration:
            filtered_list[-1][0] = midi_list_last_item[0]
        else:
            filtered_list.append(midi_list_last_item)

        return filtered_list
