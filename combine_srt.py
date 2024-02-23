import sys
import os
from config import *
import logging


def combine(origin_srt_path: str, chn_srt_path: str):
    # 如果origin包含chn的内容，直接返回
    with open(origin_srt_path, "r", encoding="utf-8") as o:
        o_lines = o.readlines()
    with open(chn_srt_path, "r", encoding="utf-8") as c:
        c_lines = c.readlines()
    target_lines = []
    o_dict = {}
    c_dict = {}
    for i in range(0, len(o_lines), CHUNK_SIZE):
        dialog_id = eval(o_lines[i])
        time_period = o_lines[i+1]
        o_content = o_lines[i+2]
        empty_line = o_lines[i+3]
        if len(empty_line) == 0:
            logging.error(f"{origin_srt_path} cannot recognize file pattern")
            return
        o_dict[dialog_id] = (time_period, o_content)

    for i in range(0, len(c_lines), CHUNK_SIZE):
        # print(i,  c_lines[i])
        dialog_id = int(c_lines[i])
        time_period = c_lines[i+1]
        c_content = c_lines[i+2]
        empty_line = c_lines[i+3]
        if len(empty_line) == 0:
            logging.error(f"{chn_srt_path} cannot recognize file pattern")
            return
        c_dict[dialog_id] = (time_period, c_content)

    for (id, value) in o_dict.items():
        if id in c_dict:
            new_str = o_dict[id][1] + c_dict[id][1]
            o_dict[id] = (o_dict[id][0], new_str)
            # o_dict[id][1] += "\n" + c_dict[id][1]

    for (k, v) in sorted(o_dict.items()):
        curr_line = str(k) + "\n" + v[0] + v[1] + "\n"
        target_lines.append(curr_line)
    
    with open("result.srt", "w", encoding="utf-8") as r:
        r.write(''.join(target_lines))


if __name__ == "__main__":
    o_path = sys.argv[1]
    c_path = sys.argv[2]
    combine(o_path, c_path)