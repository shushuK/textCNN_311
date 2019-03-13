#!usr/bin/python3
#-*- coding:utf-8 -*
import jieba
import re
from collections import Counter
import tensorflow.contrib.keras as kr
import numpy as np
import io
import json
import pickle


def read_file(f_name):

    contents, labels = [], []
    with open(f_name, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            try:
                label, content = line.strip().split('\t')
                if content:
                    contents.append(content)
                    labels.append(label)
            except:
                pass
    return contents, labels


def filter_str(filename):
    contents, labels = read_file(filename)
    filtered_contents = []
    for content in contents:
        filtering = re.compile(u'[^\u4E00-\u9FA5]')
        filtered_str = filtering.sub(r'', content)
        filtered_contents.append(filtered_str)

    return filtered_contents, labels


def fenci(finName):

    tokensList = []
    stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf8').readlines()]
    string, label = filter_str(finName)
    for s in string:
        cut_string = jieba.cut(s)
        tokens = re.split(r'[ ]', ' '.join(cut_string))
        new_tokens = [t for t in tokens if t not in stopwords]
        tokensList.append(new_tokens)

    return tokensList, label


def build_vocab(train_dir, vocab_dir, vocab_size):

    data_train, _ = fenci(train_dir)
    all_data = []
    for content in data_train:
        all_data.extend(content)
    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    words = ['<PAD>'] + list(words)
    f = open(vocab_dir, mode='w', encoding='utf8')
    f.truncate()
    f.write('\n'.join(words) + '\n')


def read_vocab(vocab_dir):

    with open(vocab_dir, encoding='utf8') as fp:
        words = [_.strip() for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))

    return words, word_to_id


def read_labels():

    f = open('jsonFiles.txt', 'r', encoding='utf8')
    cateList = set()
    for line in f.readlines():
        f_in_name = line.strip()
        label = re.split(r"[/,.]", f_in_name)[-2]
        cateList.add(label)
    categories = sorted([x for x in cateList])
    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id


def process_file(filename, vocab_dir, max_length):

    contents, labels = fenci(filename)
    word, word_to_id = read_vocab(vocab_dir)
    categories, cat_to_id = read_labels()

    contents_id, label_id = [], []
    for i in range(len(contents)):
        contents_id.append([word_to_id[x] for x in contents[i] if x in word_to_id]) # convert words in content[i] to its index id if the word in vocabulary
        label_id.append(cat_to_id[labels[i]]) # transfer labels to id
    contents_pad = kr.preprocessing.sequence.pad_sequences(contents_id, max_length, padding='post', truncating='post') # height:contents_num; width:max_length
    labels_pad = kr.utils.to_categorical(label_id, num_classes=len(cat_to_id))

    return contents_pad, labels_pad

def batch_iter(contents_pad, labels_pad, batch_size=64):
    data_len = len(contents_pad)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = contents_pad[indices]
    y_shuffle = labels_pad[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]

# if __name__ == '__main__':
