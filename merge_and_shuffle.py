#!usr/bin/python3
# #-*- coding:utf-8 -*

import os
import random
import sys

def merge_data(merge_path, f_out_name):
    f_out = open(f_out_name, 'w', encoding='utf8')
    f_out.truncate()
    for f in os.listdir(merge_path):
        f_in_path = os.path.join(merge_path, f)
        print(f_in_path)
        for line in open(f_in_path, 'r', encoding='utf8'):
            f_out.writelines(line)
    f_out.close()

def shuffle_data(raw_file_name, f_out_name):
    lines = []
    raw_file = open(raw_file_name, 'r', encoding='utf8')
    shuffled_file = open(f_out_name, 'w', encoding='utf8')
    shuffled_file.truncate()
    for line in raw_file:
        lines.append(line)
    random.shuffle(lines)
    print('shuffling...')
    for line in lines:
        shuffled_file.write(line)
    raw_file.close()
    shuffled_file.close()

if __name__ == '__main__':
    # merge_data('/opt/huawei/msk/txtData0220/', 'merged_data.txt')
    shuffle_data("/opt/huawei/msk/data0222/filtered_data.txt","/opt/huawei/msk/data0222/shuffled_filtered_data.txt")








