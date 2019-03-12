#!usr/bin/python3

#-*- coding:utf-8 -*
import json
import os
import re
import sys

def data_groupy():
    """

    :return: jsonFiles.txt
    """
    dirname = sys.argv[1]
    dirFile = open('jsonFiles.txt', 'w', encoding='utf8')
    for jFile in os.listdir(dirname):
        filedir = os.path.join(dirname, jFile)
        if os.path.isfile(filedir) and os.path.splitext(filedir)[-1] == '.json':
            dirFile.write(filedir+'\n')

if __name__ == '__main__':
    data_groupy()

