import librosa
import matplotlib.pyplot as plt
import numpy as np

from enums.enums import GlobalVariables


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
