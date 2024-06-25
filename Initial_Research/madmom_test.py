import librosa
import numpy as np
from madmom.features.beats import RNNBeatProcessor, BeatTrackingProcessor
from madmom.features.downbeats import RNNDownBeatProcessor, DBNDownBeatTrackingProcessor

def segment_song(file_path):
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)

    # Use madmom's RNN for beat detection
    beat_processor = BeatTrackingProcessor(fps=100)
    beat_activations = RNNBeatProcessor()(file_path)
    beats = beat_processor(beat_activations)

    # Use madmom's RNN for downbeat detection
    downbeat_processor = DBNDownBeatTrackingProcessor(beats_per_bar=[4, 4])
    downbeat_activations = RNNDownBeatProcessor()(file_path)
    downbeats = downbeat_processor(downbeat_activations)

    # Convert frame indices to time
    beat_times = librosa.frames_to_time(beats, sr=sr)
    downbeat_times = librosa.frames_to_time(downbeats[:, 0], sr=sr)  # only take the first column which contains times

    return beat_times, downbeat_times

# Example usage
file_path = 'Storm_Higher_Brothers_HARIKIRI.mp3'
beat_times, downbeat_times = segment_song(file_path)

print("Beat Times:", beat_times)
print("Downbeat Times:", downbeat_times)
