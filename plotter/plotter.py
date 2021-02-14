import librosa
from librosa import display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import linspace, math, sin

from miscellaneous.miscellaneous import Miscellaneous
from sound_processor.sound_processor import SoundProcessor

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
    def simple_scatter(vector, filename, xlabel='Time', ylabel='Hz'):
        plt.figure()
        plt.scatter(range(len(vector)), vector, s=10)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
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

    @staticmethod
    def generate_sin_correlation_graphs(lags, pi_parts):
        t_0 = linspace(0, 11 * math.pi, 100000)
        t_1 = linspace(0, 11 * math.pi, 100000)
        function_sin_0 = sin(t_0)
        function_sin_1 = sin(t_1)
        correlation_vector = []
        pi_part = 2 * math.pi / pi_parts
        Plotter.multiple_plot([function_sin_0, function_sin_1], 'max_autocorrelation_sin.png')
        Plotter.multiple_plot([function_sin_0], 'sin.png')
        for lag in range(lags):
            t_1 += pi_part
            function_sin_1 = sin(t_1)
            correlation = SoundProcessor.correlate(function_sin_0, function_sin_1)
            correlation_vector.append(correlation)
        Plotter.multiple_plot([function_sin_0, function_sin_1], 'end_autocorrelation_sin.png')
        Plotter.simple_plot(correlation_vector, 'correlation_vector.png', [0, 350])

    @staticmethod
    def generate_function_correlation_graphs(func_0, func_1, lags):
        correlation_vector = []
        Plotter.multiple_plot([func_0, func_1], 'max_autocorrelation.png')
        Plotter.multiple_plot([func_0], 'func.png')
        for lag in range(lags):
            func_1 = Miscellaneous.list_rotate(func_1, 1)
            correlation = SoundProcessor.correlate(func_0, func_1)
            correlation_vector.append(correlation)
        Plotter.multiple_plot([func_0, func_1], 'end_autocorrelation.png')
        Plotter.simple_plot(correlation_vector, 'correlation_vector.png', [0, 250])
