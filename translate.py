from openai import OpenAI
from tqdm import tqdm
import threading
import time

OPENAI_API = "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"
FILE_PATH = ["./03.srt"]
PROMPT_MSG = '''
you are a professional interpreter to translate a subtitle into Chinese, The user will offer the lines of the subtitles, 
and you will just need to translate the Japanese into Chinese, don't modify the line number and the time indicator (which has a format like HOUR:MIN:SEC,MS --> HOUR:MIN:SEC,MS)
'''

MODEL = "gpt-3.5-turbo"
MESSAGES = []
THREAD_COUNT = 3
CHUNK_SIZE = 4
BATCH_SIZE = 5

TOKENS_USED = 0
TARGET_LINES = 0
CURRENT_LINES  = 0
FINAL_RESULT = {}

client = OpenAI(api_key=OPENAI_API)
    

def convert_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines


def sync_main():
    result = ""
    tokens = 0
    for file in FILE_PATH:
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
    
    with open("result.srt", "w") as r:
        r.write(result)
    print(f'tokens : {tokens}') 


def multi_thread_main():
    import math
    global TARGET_LINES
    for file in FILE_PATH:
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
        with open("result.srt", "w") as f:
            result = dict(sorted(FINAL_RESULT.items()))
            content = ""
            for v in result.values():
                content += v
            f.write(content)
    print(f"{TOKENS_USED} tokens used!")



def translate_chunk(idx, all_lines):
    global TOKENS_USED, CURRENT_LINES, FINAL_RESULT
    print(f"Thread {idx} starts...")
    result = ""
    for line_idx in range(0, len(all_lines), CHUNK_SIZE*BATCH_SIZE):

        message_content = ''.join(all_lines[line_idx:min(line_idx+CHUNK_SIZE*BATCH_SIZE, len(all_lines))])
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT_MSG},
                {"role": "user", "content": message_content}
            ]
        )

        result += completion.choices[0].message.content + "\n"
        CURRENT_LINES += CHUNK_SIZE * BATCH_SIZE
        TOKENS_USED += completion.usage.total_tokens
        print(f"{CURRENT_LINES} out of {TARGET_LINES} lines translated.")
        
    FINAL_RESULT[idx] = result
    # print(result)
    # return result


if __name__ == "__main__":
    
    start = time.time()
    # sync_main()
    multi_thread_main()
    end = time.time()
    print("duration : {}".format(end-start))
