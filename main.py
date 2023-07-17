import os
import moviepy.editor as mp
import librosa
import librosa.display
import soundfile as sf
import numpy as np

# Load the video file
video = mp.VideoFileClip('Example.mp4')

# Extract the audio from the video
audio = video.audio

# Save the audio as a temporary WAV file
temp_wav_file = 'temp_audio.wav'
audio.write_audiofile(temp_wav_file)

# Load the temporary WAV file with Librosa
audio_data, sr = librosa.load(temp_wav_file)

# Perform denoising with Librosa or any other denoising method
denoised_audio = librosa.decompose.nn_filter(audio_data, aggregate=np.median, metric='cosine',width=int(librosa.time_to_samples(2, sr=sr)))

# Save the denoised audio as an MP3 file
output_audio_file = 'output_audio.mp3'
sf.write(output_audio_file, denoised_audio, sr)

# Cleanup: delete the temporary WAV file
os.remove(temp_wav_file)
