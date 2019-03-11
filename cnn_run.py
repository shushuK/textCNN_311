#!usr/bin/python3
#-*- coding:utf-8 -*
import datetime
import os
import sys
import time
from datetime import timedelta
from prepare_data import process_file, read_vocab, batch_iter, build_vocab, read_labels
import tensorflow as tf
from cnn_model import TCNNConfig, TextCNN
import numpy as np
from sklearn import metrics



def get_timeUsed(start_time):
    end_time = time.time()
    timeUsed = end_time - start_time
    return timedelta(seconds=int(round(timeUsed)))

def feed_data(x_batch, y_batch, droupout_keep_prob):
    feed_dict = {
        model.input_x: x_batch,
        model.input_y: y_batch,
        model.keep_prob: droupout_keep_prob
    }

    return feed_dict

def evaluate(sessionn, x, y):
    data_len = len(x)
    # print(data_len, "&^*&^*&^*&^*^&*")
    batch_eval = batch_iter(x, y, 64)
    lossResult = 0
    accResult = 0
    for x_batch, y_batch in batch_eval:
        batch_len = len(x_batch)
        feed_dict = feed_data(x_batch, y_batch, 1.0)
        loss, acc = sessionn.run([model.loss, model.acc], feed_dict=feed_dict)
        lossResult += loss * batch_len
        accResult += acc * batch_len
        # print(acc, "_________")
        # print(accResult,"&&&&&&&&&")

    return lossResult/data_len, accResult/data_len


def train():
    print('configuring...')

    # configure tensorboard
    tensorboard_dir = 'tensorboard0309/textcnn'
    if not os.path.exists(tensorboard_dir):
        os.makedirs(tensorboard_dir)

    # configure saver
    save_dir = 'checkpoints0310/textcnn'
    save_path = os.path.join(save_dir, 'best_val')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print('loading training data')
    start_time = time.time()
    x_train, y_train = process_file('toy_val.txt', 'vocab200k_5000.txt', 200)
    x_val, y_val = process_file('toy_test.txt', 'vocab200k_5000.txt', 200)
    timeUsed = get_timeUsed(start_time)
    print('time used:', timeUsed)

    tf.summary.scalar('loss:', model.loss)
    tf.summary.scalar('accuracy:', model.acc)
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter(tensorboard_dir)
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())

        writer.add_graph(sess.graph)

        print('training...')
        total_batch = 0
        start_time = time.time()
        best_acc_val = 0.0
        last_improved = 0
        required_improvement = 1000

        flag = False
        for epoch in range(config.num_epochs):
            print('Epoch:', epoch + 1)
            train_batch = batch_iter(x_train, y_train, config.batch_size)
            for x_train_batch, y_train_batch in train_batch:
                feed_dict = feed_data(x_train_batch, y_train_batch, config.dropout_keep_prob)

                if total_batch % config.save_per_batch == 0:
                    s = sess.run(merged_summary, feed_dict=feed_dict)
                    writer.add_summary(s, total_batch)

                if total_batch % config.print_per_batch == 0:
                    feed_dict[model.keep_prob] = 1.0
                    loss_train, acc_train = sess.run([model.loss, model.acc], feed_dict=feed_dict)
                    loss_val, acc_val = evaluate(sess, x_val, y_val)
                    if True:
                    # if acc_val > best_acc_val:
                        best_acc_val = acc_val
                        last_improved = total_batch
                        save_path = saver.save(sess=sess, save_path=save_path)
                        print(save_path)
                        improved_str = '*'
                        print("model saved...")
                    else:
                        print('sbsbsb')
                        improved_str = ''

                    msg = 'iter: {}, train loss: {}, train acc: {}, val loss:{}, val acc:{}, improved_str:{}'
                    print(msg.format(total_batch, loss_train, acc_train, loss_val, acc_val, improved_str))

                sess.run(model.optim, feed_dict=feed_dict)
                total_batch += 1

                if total_batch - last_improved > required_improvement:
                    print('no optimization for a long time, auto stopping...')
                    flag = True
                    break
            if flag:
                break

        print('time used:', get_timeUsed(start_time))

def test():
    print('loading test data...')
    start_time = time.time()
    x_test, y_test = process_file('toy_val.txt', 'vocab200k_5000.txt', 200)

    # session2 = tf.Session()
    # session2.run(tf.global_variables_initializer())
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        save_dir = 'checkpoints0310/textcnn'
        save_path = os.path.join(save_dir, 'best_val')
        loss_test, acc_test = evaluate(sess, x_test, y_test)
        msg = 'test loss:{}, test acc:{}'
        print(msg.format(loss_test, acc_test))

        saver.restore(sess=sess, save_path=tf.train.latest_checkpoint('./checkpoints0310/textcnn'))

        print('testing...')
        loss_test, acc_test = evaluate(sess, x_test, y_test)
        msg = 'test loss:{}, test acc:{}'
        print(msg.format(loss_test, acc_test))

        # batch_size = config.batch_size
        # data_len = len(x_test)
        # num_batch = int((data_len - 1) / batch_size) + 1
        # y_test_cls = np.argmax(y_test, 1) # array
        # y_pre_cls = np.zeros(shape=len(x_test), dtype=np.int32)
        total_correction = 0
        # for i in range(num_batch):
        #     startId = i * batch_size
        #     endId = min((i+1) * batch_size, data_len)
        # feed_dict = {
        #     model.input_x: x_test,
        #     model.keep_prob: 1.0
        # }
        # y_pre_cls = session.run(model.y_pred_cls, feed_dict=feed_dict)
        # correct_predictions = float(np.mean(y_test_cls == y_pre_cls))
        # print(correct_predictions)
        # total_correction += correct_predictions
            # print(i)
        # print(y_pre_cls[0: 10])
        # print(y_test_cls[0:10])
            # print(y_test_cls[startId: endId])
        # print('acc:{}'.format(total_correction/float(len(y_test_cls))))


if __name__ == '__main__':
    if not os.path.exists('vocab200k_5000.txt'):
        build_vocab('toy_train.txt', 'vocab200k_5000.txt', 10000)
    config = TCNNConfig()
    model = TextCNN(config)
    # create session

    # if sys.argv[1] == 'train':
    #     train()
    # else:
    #     test()
    # train()
    test()