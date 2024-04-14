import subsai
import os
import sys
from utils import show_time_period

@show_time_period
def transcribe(audio_path: str):
    subs_ai = subsai.SubsAI()
    model = subs_ai.create_model('openai/whisper', {'model_type': 'medium'})
    subs = subs_ai.transcribe(audio_path, model)
    # original_srts_path = os.path.splitext(audio_path)[0] + ".srt"
    original_srts_path = "result.srt"
    subs.save(original_srts_path)

if __name__ == "__main__":
    pt = sys.argv[1]
    transcribe(pt)