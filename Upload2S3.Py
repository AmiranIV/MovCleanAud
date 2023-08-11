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
    # DON'T forget to preform AWS CONIGURE!!! 
    # DON'T UPLOAD SENSITIVE DATA OR AWS credentials!
    # Replace with your own bucket name
    bucket_name = 'YOUR BUCKET NAME'
    # Initialize the S3 client
    s3 = boto3.client('s3')
    # Specify the file to upload and the S3 key (path/filename)
    s3_key = 'Master.wav'  # OR other path /Masters/Master.wav

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
    s3.upload_file(output_audio_file.name, bucket_name, s3_key)
    # Return the denoised audio file to the user
    return send_file(output_audio_file.name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

