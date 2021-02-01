import librosa
from librosa import display
import matplotlib
import matplotlib.pyplot as plt


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
    def simple_plot(vector, vector2, filename, title='', x_axis_label='', y_axis_label=''):
        plt.figure()
        plt.title(title)
        plt.xlabel(x_axis_label)
        plt.ylabel(y_axis_label)
        plt.plot(vector, vector2)
        plt.savefig(filename)

    @staticmethod
    def wave_plot(y, sr, filename):
        plt.figure()
        librosa.display.waveplot(y, sr=sr)
        plt.savefig(filename)

