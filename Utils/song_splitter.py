import os
from spleeter.separator import Separator

# Function to split a song into its components
def split_song(audio_file_path, output_path):
    # Create a separator with the desired configuration
    separator = Separator('spleeter:4stems')  # Use 'spleeter:2stems' for vocals/accompaniment, 'spleeter:4stems' for vocals/drums/bass/other

    # Separate the audio file
    separator.separate_to_file(audio_file_path, output_path)

# Example usage
audio_file_path = '/Users/tingqiwang/Desktop/AI DJ Project/Songs/Lilith1.mp3'
output_path = '/Users/tingqiwang/Desktop/AI DJ Project/Split_songs'

split_song(audio_file_path, output_path)

# List the output files
for root, dirs, files in os.walk(output_path):
    for file in files:
        print(os.path.join(root, file))
