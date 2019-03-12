#!usr/bin/python3
#-*- coding:utf-8 -*

def data_group(f_in_name, trainingFile, testFile, valFile, trainNum, testNum, valNum):
    f_train = open(trainingFile, 'w', encoding='utf8')
    f_test = open(testFile, 'w', encoding='utf8')
    f_val = open(valFile, 'w', encoding='utf8')
    f_train.truncate()
    f_test.truncate()
    f_val.truncate()
    count = 0
    f_in = open(f_in_name, 'r', encoding='utf8')
    for line in f_in:
        if count < trainNum:
            f_train.write(line)
        elif count < trainNum + testNum:
            f_test.write(line)
        elif count < trainNum + testNum + valNum:
            f_val.write(line)
        count += 1
    f_train.close()
    f_test.close()
    f_val.close()

if __name__ == '__main__':
    # data_group('shuffled_data.txt', 'train_200k.txt', 'test_20k.txt', 'val_20k.txt', 200000, 20000)
    data_group("/opt/huawei/msk/shuffled_filtered_data.txt", 'toy_train.txt', 'toy_test.txt', 'toy_val.txt', 100000, 5000, 5000)
