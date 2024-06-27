from pydub import AudioSegment

# Function to convert mp3 to wav
def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_file_path)
    
    # Export the audio in WAV format
    audio.export(wav_file_path, format="wav")

# Function to convert wav to mp3
def convert_wav_to_mp3(wav_file_path, mp3_file_path):
    # Load the WAV file
    audio = AudioSegment.from_wav(wav_file_path)
    
    # Export the audio in MP3 format
    audio.export(mp3_file_path, format="mp3")


# Example usage
mp3_file_path = "/Users/tingqiwang/Desktop/AI DJ Project/Songs/Lilith1.mp3"
wav_file_path = "/Users/tingqiwang/Desktop/AI DJ Project/Songs/Lilith1.wav"

convert_mp3_to_wav(mp3_file_path, wav_file_path)

print(f"Converted {mp3_file_path} to {wav_file_path}")
