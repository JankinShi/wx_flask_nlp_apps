# -*- coding: utf-8 -*-

class Hyperparams:
    '''Hyperparameters'''
    # data
    source_train = 'F:/code/DL/nlp/idiom/wx_idiom/app/couplets_sq2sq/data/train/in.txt'
    target_train = 'F:/code/DL/nlp/idiom/wx_idiom/app/couplets_sq2sq/data/train/out.txt'
    source_test = 'F:/code/DL/nlp/idiom/wx_idiom/app/couplets_sq2sq/data/test/in.txt'
    target_test = 'F:/code/DL/nlp/idiom/wx_idiom/app/couplets_sq2sq/data/test/out.txt'
    vocab = 'F:/code/DL/nlp/idiom/wx_idiom/app/couplets_sq2sq/data/vocab'
    
    # training
    batch_size = 128 
    lr = 0.001 # learning rate.
    logdir = 'F:/code/DL/nlp/idiom/wx_idiom/app/couplets_sq2sq/output_model'
    
    # model
    maxlen = 30 # max length for a sentence
    min_cnt = 0 # frequency threshold for vocabulary
    hidden_units = 512
    num_blocks = 6 # number of encoder/decoder blocks
    num_epochs = 20
    num_heads = 8
    dropout_rate = 0.1
    sinusoid = False # If True, use sinusoid position embedding. If false, positional embedding.
    
    
    
    
