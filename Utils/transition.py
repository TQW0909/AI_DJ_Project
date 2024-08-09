import pandas as pd
from pydub import AudioSegment
import librosa
import numpy as np
from tqdm import tqdm

# # Assume df is your DataFrame
# df = pd.DataFrame({
#     'order': [5, 3, 8, 9, 0, 12, 6, 11, 1, 2, 10, 7, 4],
#     'path': ['Songs/20min.mp3', 'Songs/Drake - In My Feelings.mp3', 'Songs/Drake,21 Savage,Project Pat - Knife Talk.mp3', 'Songs/Drake,Sexyy red,SZA - Rich Baby Daddy.mp3', 'Songs/Lil Durk,J. Cole - All My Life.mp3', 'Songs/Lil Uzi Vert - Just Wanna Rock.mp3', 'Songs/Lilith1.mp3', 'Songs/Lit Reno - STOP BREATHING!.mp3', 'Songs/Travis Scott,Kendrick Lamar - goosebumps.mp3', 'Songs/xihu.mp3', 'Songs/¥$,Kanye West,Ty Dolla $ign - VULTURES.mp3', 'Songs/艾志恒Asen - DAY1.mp3', 'Songs/艾志恒Asen,Maikon Flocka Flame - Butterflies.mp3'],
#     'bpm': [122, 91, 74, 146, 71, 150, 115, 73, 130, 128, 73, 100, 118],
#     'key': ['1A', '3B', '3A', '11A', '5B', '2A', '7A', '8B', '8A', '2A', '12A', '7A', '7A']
# })


# Function to load and normalize tracks
def load_tracks(track_paths, intro_chorus_timings):
    tracks = []
    for i, track_path in enumerate(track_paths):
        track = AudioSegment.from_file(track_path)
        intro_start, chorus_start = intro_chorus_timings[i]
        intro_start_ms = intro_start * 1000
        chorus_start_ms = chorus_start * 1000
        intro_chorus_segment = track[intro_start_ms:chorus_start_ms]
        tracks.append(intro_chorus_segment.apply_gain(-intro_chorus_segment.max_dBFS))
    return tracks

# Function to time-stretch the audio
def time_stretch(audio, rate):
    samples = np.array(audio.get_array_of_samples())
    stretched = librosa.effects.time_stretch(samples.astype(np.float32), rate=rate)
    return AudioSegment(
        stretched.tobytes(), 
        frame_rate=int(audio.frame_rate * rate), 
        sample_width=audio.sample_width, 
        channels=audio.channels
    )

# Function to gradually adjust BPM
def gradual_bpm_adjust(track, start_bpm, end_bpm, duration_ms):
    num_samples = len(track.get_array_of_samples())
    sample_rate = track.frame_rate
    times = np.linspace(0, duration_ms / 1000, num_samples)
    
    # Generate a gradually changing rate
    rates = np.linspace(start_bpm / end_bpm, 1, num_samples)
    new_samples = []
    for i, sample in enumerate(track.get_array_of_samples()):
        index = int(i * rates[i])
        if index < len(track.get_array_of_samples()):
            new_samples.append(track.get_array_of_samples()[index])
    
    new_track = AudioSegment(new_samples, frame_rate=sample_rate, sample_width=track.sample_width, channels=track.channels)
    return new_track

# Function to crossfade tracks
def crossfade_tracks(tracks, bpms, crossfade_duration=5000):
    mixed_track = tracks[0]
    for i in tqdm(range(1, len(tracks)), desc="Processing songs"):
        previous_bpm = bpms[i - 1]
        current_bpm = bpms[i]
        rate = previous_bpm / current_bpm
        
        stretched_track = time_stretch(tracks[i], rate)
        adjusted_track = gradual_bpm_adjust(stretched_track, previous_bpm, current_bpm, crossfade_duration)
        
        mixed_track = mixed_track.append(adjusted_track, crossfade=crossfade_duration)
    return mixed_track

# Function to mix tracks in optimal order
def mix_tracks_in_order(track_paths, bpm_list, intro_chorus_timings):
    print("Start mixing songs")
    normalized_tracks = load_tracks(track_paths, intro_chorus_timings)
    print("Finished normalizing tracks")
    final_mix = crossfade_tracks(normalized_tracks, bpm_list)
    print("Finished cross-fading tracks")
    return final_mix


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

    # Placeholder for intro to chorus timings for each song (in seconds)
    # Assuming each intro starts at 0 and chorus starts at a fixed time
    # Update these values based on actual timings if available
    # intro_chorus_timings = [
    #     (0, 30),   # Example timings
    #     (0, 40),   
    #     (0, 35),   
    #     (0, 45),   
    #     (0, 50),   
    #     (0, 55),   
    #     (0, 20),   
    #     (0, 25),   
    #     (0, 15),   
    #     (0, 10),   
    #     (0, 10),   
    #     (0, 10),   
    #     (0, 10)
    # ]
    print("chorus found")
    # Mix the tracks in the given order
    final_mix = mix_tracks_in_order(track_paths, bpm_list, intro_chorus_timings)

    # Export the final mix
    output_path = 'final_mix.mp3'
    final_mix.export(output_path, format='mp3')

    # Optionally, play the final mix
    # play(final_mix)

    print(f"Final mix exported to {output_path}")
