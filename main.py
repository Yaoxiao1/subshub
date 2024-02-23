import subsai
import openai
import extract_audio
import os
import logging
from translate import multi_thread_main
import sys
import time
from washing import sub_washing
import threading


def run(path: str):
    # step1 convert input file to audio
    logging.info("step1 convert input file to audio start...")
    if extract_audio.is_video_file(path):
        audio_path = os.path.splitext(path)[0] + ".mp3"
        extract_audio.extract_audio(path, audio_path)
    elif not extract_audio.is_audio_file(path):
        logging.error(f"{path} is invalid file format, exit")
        return 
    else:
        audio_path = path
    # step2 transcribe audio to original subtitle
    logging.info("step2 transcribe audio to original subtitle start...")
    subs_ai = subsai.SubsAI()
    model = subs_ai.create_model('openai/whisper', {'model_type': 'small'})
    subs = subs_ai.transcribe(audio_path, model)
    original_srts_path = os.path.splitext(audio_path)[0] + ".srt"
    subs.save(original_srts_path)
    os.remove(audio_path)

    # step3 washing the original title
    logging.info("step3 washing the original title start...")
    sub_washing(original_srts_path)
    
    # step4 translate original subtitle to Chinese
    # logging.info("step4 translate original subtitle to Chinese start...")
    # multi_thread_main([original_srts_path])

    # step4 combine original and translated subtitles
    # TODO: combine original and translated subtitles




if __name__ == "__main__":
    all_file = sys.argv[1:]
    logging.info("start translating...")
    for file in all_file:
        logging.info("start traslating {}".format(file))
        run(file)
        logging.info("finished traslating {}".format(file))
        time.sleep(180)
    logging.info("all files translated!")