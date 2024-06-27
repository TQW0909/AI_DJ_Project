'''import librosa 
# 加载音频文件
audio_path = 'storm.mp3'
audio, sr = librosa.load(audio_path)

tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)
# 输出节奏信息
print(f'Tempo: {tempo} BPM')
print(f'Beat frames: {beat_frames}')'''

'''from madmom.features.chords import CNNChordFeatureProcessor  
from madmom.features.chords import CRFChordRecognitionProcessor

featproc = CNNChordFeatureProcessor()
decode = CRFChordRecognitionProcessor()
filename1= 'storm.wav'
feats = featproc(filename1)
reout = decode(feats)
print(reout)
'''

'''import librosa
import numpy as np
from madmom.features.beats import RNNBeatProcessor, BeatTrackingProcessor
from madmom.features.downbeats import RNNDownBeatProcessor, DBNDownBeatTrackingProcessor
import pyximport
pyximport.install()


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
file_path = 'storm.wav'
beat_times, downbeat_times = segment_song(file_path)

print("Beat Times:", beat_times)
print("Downbeat Times:", downbeat_times)
'''

'''from pychorus import find_and_output_chorus

chorus_start_sec = find_and_output_chorus("band4band.wav", "test.wav")
print()'''
