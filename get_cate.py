#!usr/bin/python3

# #-*- coding:utf-8 -*
import json

# f = open('jsonFiles.txt', 'r', encoding='utf8')
# for l in f.readlines():
#     f_in_name = l.strip()
#     f_in = open(f_in_name, 'r', encoding='utf8')
#     obj = json.loads(f_in.readline())
#     category = obj['category']
#     cateList = []
#     if category not in cateList:
#         cateList.append(category)
# print(cateList)

def read_category(file_name_list):
    f = open(file_name_list, 'r', encoding='utf8')
    cateList = []
    for line in f.readlines():
        f_in_name = line.strip()
        print(f_in_name)
        f_in = open(f_in_name, 'r', encoding='utf8')
        line = f_in.readline()
        obj = json.loads(line)
        category = obj['category']
        # category = list(category)
        if category not in cateList:
            cateList.append(category)
    return cateList

result = read_category('jsonFiles.txt')
print(result)