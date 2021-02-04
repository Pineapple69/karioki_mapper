from numpy import linspace, math, sin

from plotter.plotter import Plotter
from sound_processor.sound_processor import SoundProcessor


class Miscellaneous:
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
