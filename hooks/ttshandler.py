import os
import time
import requests
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import speech_recognition as sr
from gtts import gTTS

# Configuration
input_folder = 'recordings'
output_folder = 'recordings/converted'
server_url = 'http://192.168.0.*/play'
base_url = 'http://192.168.0.*:5000/vl/hooks/recordings/converted/'

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.wav') and '_pcm' not in event.src_path:
            print(f"New .wav file detected: {event.src_path}")
            self.process_wav_file(event.src_path)

    def process_wav_file(self, file_path):
        # Convert the .wav file to PCM format using FFmpeg
        pcm_file_path = file_path.replace('.wav', '_pcm.wav')
        try:
            # Use FFmpeg to convert the file to 16-bit PCM WAV format
            command = [
                'ffmpeg', '-i', file_path, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', pcm_file_path
            ]
            subprocess.run(command, check=True)
            print(f"Converted {file_path} to PCM format: {pcm_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {file_path} to PCM format using FFmpeg: {e}")
            return
        except Exception as e:
            print(f"Unexpected error during conversion: {e}")
            return

        # Convert speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(pcm_file_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                print(f"Recognized text: {text}")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return

        # Convert text to speech and save as mp3
        tts = gTTS(text=text, lang='en')
        mp3_filename = os.path.basename(file_path).replace('.wav', '.mp3')
        mp3_path = os.path.join(output_folder, mp3_filename)
        tts.save(mp3_path)
        print(f"Converted text to speech and saved to {mp3_path}")

        # Make GET request to the server
        recording_url = base_url + mp3_filename
        response = requests.get(f"{server_url}?u={recording_url}")
        if response.status_code == 200:
            print("Successfully notified the server.")
        else:
            print("Failed to notify the server.")

        # Clean up temporary _pcm.wav file
        if os.path.exists(pcm_file_path):
            os.remove(pcm_file_path)
            print(f"Deleted temporary file: {pcm_file_path}")

if __name__ == "__main__":
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=input_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
