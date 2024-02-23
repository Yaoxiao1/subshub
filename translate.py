from openai import OpenAI
from tqdm import tqdm
import threading
import time
from config import *
import logging
import os
import sys
from utils import show_time_period


TOKENS_USED = 0
TARGET_LINES = 0
CURRENT_LINES  = 0
FINAL_RESULT = {}

client = OpenAI(api_key=OPENAI_API)
    

def convert_file_to_list(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines


def sync_main(file_path: list):
    result = ""
    tokens = 0
    for file in file_path:
        srt_chn = os.path.splitext(file)[0] + "_CHN.srt"
        all_lines = convert_file_to_list(file)
        line_idx = 0
        for line_idx in tqdm(range(0, len(all_lines), CHUNK_SIZE*BATCH_SIZE)):

        # while line_idx < len(all_lines):

            message_content = ''.join(all_lines[line_idx:min(line_idx+CHUNK_SIZE*BATCH_SIZE, len(all_lines))])
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": PROMPT_MSG},
                    {"role": "user", "content": message_content}
                ]
            )
            # line_idx += CHUNK_SIZE * BATCH_SIZE
            result += completion.choices[0].message.content + "\n"
            tokens += completion.usage.total_tokens
    
        with open(srt_chn, "w") as r:
            r.write(result)
    logging.debug(f'tokens : {tokens}') 

@show_time_period
def multi_thread_main(file_path : list):
    import math
    global TARGET_LINES
    for file in file_path:
        TARGET_LINES = 0
        srt_chn = os.path.splitext(file)[0] + "_CHN.srt"
        handlers = []
        all_lines = convert_file_to_list(file)
        # result = ""
        TARGET_LINES = len(all_lines)
        sentences_number = len(all_lines) // 4
        epoch_size = math.ceil(sentences_number / THREAD_COUNT)
        for i in range(THREAD_COUNT):
            start_idx = i*epoch_size * 4
            end_idx = min((i+1)*epoch_size, sentences_number) * 4
            lines = all_lines[start_idx:end_idx].copy()
            x = threading.Thread(target=translate_chunk, 
                                 args=(i, lines))
            x.start()
            time.sleep(0.5)
            handlers.append(x)
        for handler in handlers:
            handler.join()
        with open(srt_chn, "w", encoding="utf-8") as f:
            result = dict(sorted(FINAL_RESULT.items()))
            content = ""
            for v in result.values():
                content += v
            f.write(content)
    logging.info(f"{TOKENS_USED} tokens used!")



def translate_chunk(idx: int, all_lines: list):
    global TOKENS_USED, CURRENT_LINES, FINAL_RESULT
    logging.debug(f"Thread {idx} starts...")
    result = ""
    for line_start_idx in range(0, len(all_lines), CHUNK_SIZE*BATCH_SIZE):
        line_end_idx = min(line_start_idx+CHUNK_SIZE*BATCH_SIZE, len(all_lines))
        message_content = ''.join(all_lines[line_start_idx:line_end_idx])
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT_MSG},
                {"role": "user", "content": message_content}
            ]
        )

        result += completion.choices[0].message.content + "\n\n"
        CURRENT_LINES += line_end_idx - line_start_idx + 1
        TOKENS_USED += completion.usage.total_tokens
        logging.debug(f"{CURRENT_LINES} out of {TARGET_LINES} lines translated.")
    FINAL_RESULT[idx] = result


if __name__ == "__main__":
    
    start = time.time()
    file_path = sys.argv[1]
    # sync_main()
    multi_thread_main([file_path])
    end = time.time()
    print("duration : {}".format(end-start))
