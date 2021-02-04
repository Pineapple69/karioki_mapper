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
    def simple_plot(vector, filename, xlim=None, ylim=None):
        plt.figure()
        plt.plot(vector)
        if not xlim is None:
            plt.xlim(xlim)
        if not ylim is None:
            plt.ylim(ylim)
        plt.savefig(filename)

    @staticmethod
    def simple_scatter(vector, filename):
        plt.figure()
        plt.scatter(range(len(vector)), vector, s=10)
        plt.xlabel('Time')
        plt.ylabel('Hz')
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

    @staticmethod
    def multiple_plot(func_list, filename):
        plt.figure()
        for index, func in enumerate(func_list):
            plt.plot(func)
        plt.xlabel('Time [µs]')
        plt.savefig(filename)

    @staticmethod
    def wave_plot(y, sr, filename):
        plt.figure()
        librosa.display.waveplot(y, sr=sr)
        plt.savefig(filename)
