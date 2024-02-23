import os
import sys
import logging
import re

from utils import show_time_period

@show_time_period
def sub_washing(sub_path : str):
    sentence_gap = 4
    new_lines = []
    last_content = ""
    elimiated_lines = 0
    with open(sub_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    for idx in range(0, len(all_lines), sentence_gap):
        _sentence_number = all_lines[idx]
        _time_range = all_lines[idx+1]
        content = all_lines[idx+2]
        _empty_line = all_lines[idx+3]
        if should_skip(content, prev_content=last_content):
            elimiated_lines += sentence_gap
            continue
        last_content = content
        new_lines.extend(all_lines[idx:idx+sentence_gap])
    with open(sub_path, "w", encoding="utf-8") as f:
        f.write(''.join(new_lines))
    save_to_home_dir(new_lines, sub_path)
    logging.warn(f"elimiated lines: {elimiated_lines}") if elimiated_lines > 0 else None


def should_skip(content:str, prev_content:str) -> bool:
    punctuation_pattern = r'[^\w]'
    if re.sub(punctuation_pattern, '', content) == re.sub(punctuation_pattern, '', prev_content):
        return True
    if len(content) > 50:
        return True
    return False


def save_to_home_dir(new_lines: list, origin_subpath: str):
    target_dir = os.path.join(os.path.expanduser("~"), "Documents/subtitles")
    base_name = os.path.basename(origin_subpath)
    new_subpath = os.path.join(target_dir, base_name)
    with open(new_subpath, "w", encoding="utf-8") as f:
        f.write(''.join(new_lines))



if __name__ == "__main__":
    sub_path = sys.argv[1]
    sub_washing(sub_path)
        