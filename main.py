import subsai
import openai
import extract_audio
import os
import logging
import translate
import sys


def run(video_path: str):
    # step1 convert input file to audio
    if not extract_audio.is_video_file(video_path):
        logging.error("{} is not a video file".format(video_path))
        return 
    audio_path = os.path.splitext(video_path)[0] + ".mp3"
    extract_audio.extract_audio(video_path, audio_path)

    # step2 transcribe audio to text
    subs_ai = subsai.SubsAI()
    model = subs_ai.create_model('openai/whisper', {'model_type': 'base'})
    subs = subs_ai.transcribe(audio_path, model)
    original_srts_path = os.path.splitext(audio_path)[0] + ".srt"
    subs.save(original_srts_path)
    
    # step3 translate original subtitle to Chinese
    translate.multi_thread_main([original_srts_path])

    # step4 combine original and translated subtitles
    # TODO: combine original and translated subtitles



if __name__ == "__main__":
    all_file = sys.argv[1:]
    logging.info("start translating...")
    for file in all_file:
        logging.info("start traslating {}".format(file))
        run(file)
        logging.info("finished traslating {}".format(file))
    logging.info("all files translated!")