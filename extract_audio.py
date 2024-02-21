from moviepy.editor import VideoFileClip
import os

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def is_video_file(file_path):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg']
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension in video_extensions:
        return True
    else:
        return False

# Example usage


if __name__ == "__main__":
    video_path = "./test0.webm"
    audio_path = "./test0.mp3"
    extract_audio(video_path, audio_path)