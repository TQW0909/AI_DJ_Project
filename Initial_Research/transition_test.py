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

def gradual_bpm_adjust(audio, sr, target_bpm, original_bpm, duration = 5):
    samples = audio.shape[0]
    time_stretched_audio = librosa.effects.time_stretch(audio, rate=target_bpm / original_bpm)

    # Create an array to hold the gradually adjusted audio
    adjusted_audio = np.zeros_like(time_stretched_audio)

    # Calculate the number of samples to change BPM
    change_samples = int(duration * sr)

    for i in range(change_samples):
        factor = (i / change_samples) * ((original_bpm - target_bpm) / target_bpm) + 1
        adjusted_audio[i] = librosa.effects.time_stretch(time_stretched_audio[i:i+1], rate=factor)

    # Append the rest of the audio unchanged
    adjusted_audio[change_samples:] = time_stretched_audio[change_samples:]

    return adjusted_audio

def linear_crossfade(audio1, audio2, sr, transition_duration, transition_point, bpms):
    # Calculate the number of samples for the transition
    transition_samples = int(transition_duration * sr)
    
    # Determine the midpoint of both audio files
    point1 = transition_point * sr
    point2 = 0.00 * sr
    
    # Define the segments to crossfade
    start1 = int(point1)
    end1 = int(start1 + transition_samples)
    start2 = int(point2)
    end2 = int(start2 + transition_samples)

    # Create a linear crossfade
    crossfade = np.linspace(0, 0.5, transition_samples)
    crossfade_audio1 = audio1[start1:end1] * (1 - crossfade)
    crossfade_audio2 = audio2[start2:end2] * (crossfade + 0.7)

    audio2 = gradual_bpm_adjust(audio2, sr, bpms[0], bpms[1])

    # Combine the audio segments
    mixed_audio = np.concatenate((audio1[:start1], crossfade_audio1 + crossfade_audio2, audio2[end2:]))
    
    return mixed_audio

def mix_songs(df):

    # Sort DataFrame by order
    df = df.sort_values(by='order')

    # Extract the required columns
    track_paths = df['path'].tolist()
    bpm_list = df['bpm'].tolist()
    key_list = df['key'].tolist()
    info_list =df['info'].tolist()

    # Function to find the chorus that immediately follows a verse
    intro_chorus_timings = []

    for song in info_list:
        segments = song.segments

        for i in range(len(segments) - 1):
            if segments[i].label == "verse" and segments[i + 1].label == "chorus":
                intro_chorus_timings.append((0, segments[i + 1].start))
                break  # Stop after finding the first chorus following a verse
    
    print("chorus found")

    curr_song, sr1 = load_audio(track_paths[0])

    mixed_song_length = intro_chorus_timings[0][1]


    for i in range(len(track_paths) - 2):

        next_song, sr2 = load_audio(track_paths[i + 1])

        # Ensure both audios have the same sample rate
        assert sr1 == sr2, "Sample rates do not match!"

        target_bpm = bpm_list[i]

        adjusted_audio2 = change_bpm(next_song, sr2, bpm_list[i + 1], target_bpm)

        transition_duration = 1 / (target_bpm / 60)  *  4 * 8 # seconds

        mixed_audio = linear_crossfade(curr_song, adjusted_audio2, sr1, transition_duration, mixed_song_length, (bpm_list[i + 1], target_bpm))

        curr_song = mixed_audio

        mixed_song_length += intro_chorus_timings[i + 1][1]

    # Save the mixed audio to a file
    output_file = 'mixed_song.wav'
    save_audio(mixed_audio, sr1, output_file)
    print(f"Mixed audio saved to {output_file}")


        
    

# def main():
#     # Load the two audio files
#     file1 = '../Songs/20min.mp3'
#     file2 = '../Songs/xihu.mp3'
    
#     audio1, sr1 = load_audio(file1)
#     audio2, sr2 = load_audio(file2)
    
#     # Ensure both audios have the same sample rate
#     assert sr1 == sr2, "Sample rates do not match!"

#     original_bpm1 = find_bpm(audio1, sr1)
#     original_bpm2 = find_bpm(audio2, sr2)

#     target_bpm = original_bpm1 # min(original_bpm1, original_bpm2) + (abs(original_bpm1 - original_bpm2) / 2.0)
#     # adjusted_audio1 = change_bpm(audio1, sr1, original_bpm1[0], target_bpm[0])
#     adjusted_audio2 = change_bpm(audio2, sr2, original_bpm2[0], target_bpm[0])

#     # Define the duration of the transition in seconds
#     transition_duration = 1 / (target_bpm[0] / 60)  *  4 * 8 # seconds
#     print(transition_duration)
#     # Create the mixed audio with a linear harmonic transition
#     mixed_audio = linear_crossfade(audio1, adjusted_audio2, sr1, transition_duration)
    
#     # Save the mixed audio to a file
#     output_file = 'mixed_song.wav'
#     save_audio(mixed_audio, sr1, output_file)
#     print(f"Mixed audio saved to {output_file}")

# main()

 