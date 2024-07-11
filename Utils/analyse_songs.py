import allin1

# You can analyze a single file:
result = allin1.analyze('your_audio_file.wav')

# Or multiple files:
results = allin1.analyze(['your_audio_file1.wav', 'your_audio_file2.mp3'])

result = allin1.analyze(
  'your_audio_file.wav',
  out_dir='./struct',
)