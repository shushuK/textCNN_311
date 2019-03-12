#!usr/bin/python3
#-*- coding:utf-8 -*
import json
import os
import random

import re

html_pattern = re.compile('<.*?>')
def clean_html(raw_html):
    clean_text = re.sub(html_pattern, '', raw_html)
    return clean_text

def json2txt(f_in_name,f_out_name):
    """
    :param:
    :return: file data in dict
    """

    f_in = open(f_in_name, 'r', encoding='utf8')
    f_out = open(f_out_name, 'w', encoding='utf8')
    label = re.split(r"[/,.]", f_in_name)[-2]
    count = 0
    f_out.truncate()
    for line in f_in:
        if count < 10000:
            obj = json.loads(line)
            # category = obj.get('category')
            title = obj.get('title')
            text = obj.get('text', 'not exist')
            title = clean_html(title).strip()
            text = clean_html(text).strip()
            f_out.write(label + '\t' + title + text + '\n')
            count += 1
    f_in.close()
    f_out.close()

if __name__ == '__main__':
    f = open('jsonFiles.txt', 'r', encoding='utf8')
    for line in f.readlines():
        f_in_name = line.strip()
        f_out_name = os.path.join('/opt/huawei/msk/txtData0220/', f_in_name.split('/')[-1].strip().replace('.json', '.txt'))
        json2txt(f_in_name, f_out_name)
        print(f_out_name)
    f.close()