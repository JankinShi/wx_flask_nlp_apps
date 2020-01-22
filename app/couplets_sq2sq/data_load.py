# -*- coding: utf-8 -*-

from hyperparams import Hyperparams as hp
import tensorflow as tf
import numpy as np
import sys

def load_vocab():
    vocab = [line.split()[0] for line in open('F:/code/DL/nlp/idiom/wx_idiom/app/couplets_sq2sq/data/vocabs.txt', 'r', encoding="utf-8") ]  #if int(line.split('\n')[1])>=hp.min_cnt
    word2idx = {word: idx for idx, word in enumerate(vocab)}
    idx2word = {idx: word for idx, word in enumerate(vocab)}
    return word2idx, idx2word

def create_data(source_sents, target_sents):
    char2idx, idx2char = load_vocab()

    # Index
    x_list, y_list, Sources, Targets = [], [], [], []
    for source_sent, target_sent in zip(source_sents, target_sents):
        x = [char2idx.get(word, 1) for word in (source_sent.strip() + " </S>").split()] # 1: OOV, </S>: End of Text
        y = [char2idx.get(word, 1) for word in (target_sent.strip() + " </S>").split()]
        if max(len(x), len(y)) <= hp.maxlen:
            x_list.append(np.array(x))
            y_list.append(np.array(y))
            Sources.append(source_sent)
            Targets.append(target_sent)
    
    # Pad      
    X = np.zeros([len(x_list), hp.maxlen], np.int32)
    Y = np.zeros([len(y_list), hp.maxlen], np.int32)
    for i, (x, y) in enumerate(zip(x_list, y_list)):
        X[i] = np.lib.pad(x, [0, hp.maxlen-len(x)], 'constant', constant_values=(0, 0))
        Y[i] = np.lib.pad(y, [0, hp.maxlen-len(y)], 'constant', constant_values=(0, 0))
    
    return X, Y, Sources, Targets

def create_source_data(source_sents): 
    char2idx, idx2char = load_vocab()
    # Index
    x_list, Sources = [], []
    for source_sent in source_sents:
        source_sent = [char for char in source_sent.strip()]
        x = [char2idx.get(word, 1) for word in (source_sent + ["</S>"])] # 1: OOV, </S>: End of Text
        if len(x) <= hp.maxlen:
            x_list.append(np.array(x))
            Sources.append(source_sent)
        else:
            x_list.append(np.array(x[:hp.maxlen]))
            Sources.append(source_sent[:hp.maxlen])
    
    # Pad      
    X = np.zeros([len(x_list), hp.maxlen], np.int32)
    for i, x in enumerate(x_list):
        X[i] = np.lib.pad(x, [0, hp.maxlen-len(x)], 'constant', constant_values=(0, 0))
    
    return X, Sources

def load_train_data():
    source_sents = [line for line in open(hp.source_train, 'r', encoding="utf-8")]
    target_sents = [line for line in open(hp.target_train, 'r', encoding="utf-8")]
    
    X, Y, Sources, Targets = create_data(source_sents, target_sents)
    return X, Y

def load_test_data():
    source_sents = [line for line in open(hp.source_test, 'r', encoding="utf-8")]
    target_sents = [line for line in open(hp.target_test, 'r', encoding="utf-8")]
    
    X, Y, Sources, Targets = create_data(source_sents, target_sents)
    return X, Y, Sources, Targets

def load_source_data(test_path):
    source_sents = [line for line in open(test_path, 'r')]
    
    X, Sources= create_source_data(source_sents)
    return X, Sources

def get_batch_data():
    # Load data
    X, Y = load_train_data()    
    print("Load %d pairs of couplet." % (len(X)))
    # calc total batch count
    num_batch = (len(X) // hp.batch_size) if (len(X) // hp.batch_size)>0 else 1
    
    # Convert to tensor
    X = tf.convert_to_tensor(X, tf.int32)
    Y = tf.convert_to_tensor(Y, tf.int32)
    
    # Create Queues
    input_queues = tf.train.slice_input_producer([X, Y])
            
    # create batch queues
    x, y = tf.train.shuffle_batch(input_queues,
                                num_threads=8,
                                batch_size=hp.batch_size, 
                                capacity=hp.batch_size*64,   
                                min_after_dequeue=hp.batch_size*32, 
                                allow_smaller_final_batch=False)
    
    return x, y, num_batch # (N, T), (N, T), ()

