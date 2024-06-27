import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment

def load_audio(file_path, sr=44100):
    y, sr = librosa.load(file_path, sr=sr)
    return y, sr

def find_bpm(audio, sr):
    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)
    return tempo

def change_bpm(audio, sr, original_bpm, target_bpm):
    # Calculate the tempo change factor
    tempo_factor = target_bpm / original_bpm
    # Apply the tempo change
    return librosa.effects.time_stretch(audio, rate = tempo_factor)

def save_audio(y, sr, output_path):
    sf.write(output_path, y, sr)

def linear_crossfade(audio1, audio2, sr, transition_duration):
    # Calculate the number of samples for the transition
    transition_samples = int(transition_duration * sr)
    
    # Determine the midpoint of both audio files
    point1 = 16.3 * sr
    point2 = 0.0
    
    # Define the segments to crossfade
    start1 = int(point1)
    end1 = int(start1 + transition_samples)
    start2 = int(point2)
    end2 = int(start2 + transition_samples)

    # Create a linear crossfade
    crossfade = np.linspace(0, 0.5, transition_samples)
    crossfade_audio1 = audio1[start1:end1] * (1 - crossfade)
    crossfade_audio2 = audio2[start2:end2] * (crossfade + 0.5)

    # Combine the audio segments
    mixed_audio = np.concatenate((audio1[:start1], crossfade_audio1 + crossfade_audio2, audio2[end2:]))
    
    return mixed_audio

def main():
    # Load the two audio files
    file1 = '20min.mp3'
    file2 = 'xihu.mp3'
    
    audio1, sr1 = load_audio(file1)
    audio2, sr2 = load_audio(file2)
    
    # Ensure both audios have the same sample rate
    assert sr1 == sr2, "Sample rates do not match!"

    original_bpm1 = find_bpm(audio1, sr1)
    original_bpm2 = find_bpm(audio2, sr2)
    target_bpm = min(original_bpm1, original_bpm2) + (abs(original_bpm1 - original_bpm2) / 2.0)
    adjusted_audio1 = change_bpm(audio1, sr1, original_bpm1[0], target_bpm[0])
    adjusted_audio2 = change_bpm(audio2, sr2, original_bpm2[0], target_bpm[0])
    # Define the duration of the transition in seconds
    transition_duration = 1 / (target_bpm[0] / 60)  *  4 * 8 # seconds
    print(transition_duration)
    # Create the mixed audio with a linear harmonic transition
    mixed_audio = linear_crossfade(adjusted_audio1, adjusted_audio2, sr1, transition_duration)
    
    # Save the mixed audio to a file
    output_file = 'mixed_song.wav'
    save_audio(mixed_audio, sr1, output_file)
    print(f"Mixed audio saved to {output_file}")

main()

 