from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import moviepy.editor as mp
import librosa
import soundfile as sf
import tempfile
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    # Check if a file was uploaded
    if 'video_file' not in request.files:
        return 'No file uploaded'

    video_file = request.files['video_file']

    # Generate a secure filename and save the uploaded video file to a temporary location
    temp_video_file = tempfile.NamedTemporaryFile(suffix='.mov')
    video_file.save(temp_video_file.name)

    # Extract the audio from the video
    video = mp.VideoFileClip(temp_video_file.name)
    audio = video.audio

    # Save the audio as a temporary WAV file
    temp_audio_file = tempfile.NamedTemporaryFile(suffix='.wav')
    audio.write_audiofile(temp_audio_file.name)

    # Load the temporary WAV file with Librosa
    audio_data, sr = librosa.load(temp_audio_file.name)

    # Perform denoising using Librosa
    denoised_audio, _ = librosa.effects.trim(audio_data)

    # Save the denoised audio as an MP3 file in a temporary location
    output_audio_file = tempfile.NamedTemporaryFile(suffix='.mp3')
    sf.write(output_audio_file.name, denoised_audio, sr)

    # Return the denoised audio file to the user
    return send_file(output_audio_file.name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
import pkg_resources

# Get a list of all installed packages
installed_packages = pkg_resources.working_set

# Define the path of the requirements text file
requirements_file = "requirements.txt"

# Open the file in write mode
with open(requirements_file, "w") as file:
    # Iterate over the installed packages
    for package in installed_packages:
        # Write the package name and version to the file
        file.write(f"{package.key}=={package.version}\n")
