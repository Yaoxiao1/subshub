from moviepy.editor import VideoFileClip

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

# Example usage
video_path = "path/to/video.mp4"
audio_path = "path/to/audio.wav"

extract_audio(video_path, audio_path)