import librosa
from librosa import display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.use('Agg')


class Plotter:
    @staticmethod
    def spectrogram_plot(db, y, sr, hop_length, filename):
        plt.figure()
        librosa.display.specshow(db, y_axis='log', sr=sr, hop_length=hop_length, x_axis='time')
        plt.colorbar()
        librosa.feature.melspectrogram(y=y, sr=sr)
        plt.tight_layout()
        plt.savefig(filename)

    @staticmethod
    def simple_plot(vector, filename):
        plt.figure()
        # plt.plot(vector)
        plt.scatter(range(len(vector)), vector)
        plt.savefig(filename)

    @staticmethod
    def plot_hann_window(filename):
        window = np.hanning(51)
        plt.figure()
        plt.plot(window)
        plt.title("Hann window")
        plt.ylabel("Amplitude")
        plt.xlabel("Sample")
        plt.savefig(filename)
