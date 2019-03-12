#-*- coding:utf-8 -*
# !encoding:utf8

import json
import sys
import random

fw = open("/opt/huawei/msk/data0222/filtered_data.txt", "w")

fr = open("/opt/huawei/msk/shuffled_data.txt", "r")

utilMap = {}
data = {}
rowCount = 50000
minRow = 9000

for line in fr:
    # print(type(line))
    try:
        line = line.strip("\n").strip() # list
        label = line.split("\t")[0].split(",") # list
        # if len(labels) > 1:
        #     continue
        label = label[0] # string
        content = line.split("\t")[1].strip()
        if content == "":
            continue
        if label in utilMap:
            if utilMap[label] < rowCount:
                utilMap[label] += 1
            else:
                continue
        else:
            utilMap[label] = 1
        if label in data:
            data[label].append(line)
        else:
            data[label] = [line]
    except Exception as e:
        print(line)
        print(e)
        continue
#
for key, value in data.items():
    try:
        if len(value) < minRow:
            print("%s:%s" % (key, len(value)))
            continue
        else:
            fw.write("\n".join(value)) # value: line
    except Exception as e:
        print(e)

print(json.dumps(utilMap, indent=4))
