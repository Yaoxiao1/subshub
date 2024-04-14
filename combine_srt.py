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
    i = 0
    while i < len(o_lines):
    # for i in range(0, len(o_lines), CHUNK_SIZE-1):
        while  i < len(o_lines) and len(o_lines[i].strip()) == 0:
            i += 1
        if i >= len(o_lines):
            break
        # print(i, o_lines[i].strip())
        dialog_id = int(o_lines[i])
        time_period = o_lines[i+1]
        o_content = o_lines[i+2]
        o_dict[dialog_id] = (time_period, o_content)
        i += 3

    i = 0
    while i < len(c_lines):
    # for i in range(0, len(c_lines), CHUNK_SIZE-1):
        # print(i,  c_lines[i])
        while i < len(c_lines) and len(c_lines[i].strip()) == 0 :
            i += 1
        if i >= len(c_lines):
            break
        dialog_id = int(c_lines[i].strip())
        time_period = c_lines[i+1]
        j = 2
        c_content = ""
        while i+j < len(c_lines) and len(c_lines[i+j].strip()) > 0:
            c_content += c_lines[i+j]
            j += 1
        
        c_dict[dialog_id] = (time_period, c_content)
        i += j

    for (id, value) in o_dict.items():
        if id in c_dict:
            new_str = o_dict[id][1] + c_dict[id][1]
            o_dict[id] = (o_dict[id][0], new_str)
            # o_dict[id][1] += "\n" + c_dict[id][1]

    for (k, v) in sorted(o_dict.items()):
        curr_line = str(k) + "\n" + v[0] + v[1] + "\n"
        target_lines.append(curr_line)
    combined_srt = os.path.splitext(origin_srt_path)[0] + "_combined.srt"
    
    with open(combined_srt, "w", encoding="utf-8") as r:
        r.write(''.join(target_lines))


if __name__ == "__main__":
    o_path = sys.argv[1]
    c_path = sys.argv[2]
    combine(o_path, c_path)