import os
from madmom.features.key import CNNKeyRecognitionProcessor

# Define Camelot key profiles (12 major and 12 minor keys)
camelot_keys = [
    '1A', '2A', '3A', '4A', '5A', '6A', '7A', '8A', '9A', '10A', '11A', '12A',  # Minor keys
    '1B', '2B', '3B', '4B', '5B', '6B', '7B', '8B', '9B', '10B', '11B', '12B'   # Major keys
]

# Mapping from madmom key prediction to Camelot notation
key_map = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', # Major keys
    'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm' # Minor keys
]

camelot_key_map = {
    'C': '8B', 'C#': '3B', 'D': '10B', 'D#': '5B', 'E': '12B', 'F': '7B', 'F#': '2B', 'G': '9B', 'G#': '4B', 'A': '11B', 'A#': '6B', 'B': '1B',
    'Cm': '5A', 'C#m': '12A', 'Dm': '7A', 'D#m': '2A', 'Em': '9A', 'Fm': '4A', 'F#m': '11A', 'Gm': '6A', 'G#m': '1A', 'Am': '8A', 'A#m': '3A', 'Bm': '10A'
}

def detect_harmonic_key(audio_path):
    # Use madmom's key detection function
    key_detector = CNNKeyRecognitionProcessor()
    key_prediction = key_detector(audio_path)
    
    # Get the key with the highest probability
    predicted_key_index = key_prediction.argmax()
    predicted_key = key_map[predicted_key_index]
    
    # Convert the predicted key to Camelot notation
    camelot_key = camelot_key_map[predicted_key]
    
    return camelot_key

def process_folder(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav") or filename.endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)
            detected_key = detect_harmonic_key(file_path)
            results.append({'file': filename, 'key': detected_key})
    return results

# Example usage
folder_path = '../Songs/'
detected_keys = process_folder(folder_path)
for result in detected_keys:
    print(f"File: {result['file']}, Detected Key: {result['key']}")
