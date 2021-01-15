import librosa
import numpy as np


class SoundProcessor:

    @staticmethod
    def detect_pitch_stft(y, n_fft, hop_length):
        s_db = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length)), ref=np.max)
        return s_db

    @staticmethod
    def detect_pitch_piptrack(y, sr):
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        return {pitches: pitches, magnitudes: magnitudes}

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
        for frame_number in range(frames_number):
            frame = decibel_matrix[:, frame_number]
            max_frame_magnitude = frame.max()
            max_frame_magnitude_index = np.where(frame == max_frame_magnitude)
            if max_frame_magnitude > -80:
                extracted_frequencies[frame_number] = fft_frequencies[max_frame_magnitude_index]
        return extracted_frequencies

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
        return bpm * seconds / 60
