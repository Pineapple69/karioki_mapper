import librosa


def bpm_detector():
    filename = librosa.example('nutcracker')
    y, sr = librosa.load(filename)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
