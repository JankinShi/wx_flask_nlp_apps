# -*- coding: utf-8 -*-

import os
import tensorflow as tf
import numpy as np
import sys
from hyperparams import Hyperparams as hp
from data_load import load_source_data, load_vocab
from train import Graph

def test(path):
    # Load graph
    g = Graph(is_training=False)
    print("Graph loaded")

    # Load data
    X, Sources = load_source_data(path)
    char2idx, idx2char = load_vocab()


    # Start session
    with g.graph.as_default():
        sv = tf.train.Supervisor()
        with sv.managed_session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:

            ## Get model name
            mname = "model_epoch_03_gs_18054" # model name

            ## Restore parameters
            sv.saver.restore(sess, os.path.join(hp.logdir, mname))
            print("Restored!")


            ## Inference
            if not os.path.exists('results'): os.mkdir('results')
            with open("results/" + mname + "_test", "w") as fout:
                x = X
                sources = Sources
                ### Autoregressive inference
                preds = np.zeros((len(x), hp.maxlen), np.int32)
                for j in range(hp.maxlen):
                    _preds = sess.run(g.preds, {g.x: x, g.y: preds})
                    preds[:, j] = _preds[:, j]

                ### Write to file
                for source, pred in zip(sources, preds): # sentence-wise
                    got = "".join(idx2char[idx] for idx in pred).split("</S>")[0].strip()
                    fout.write("- 上联: " + ''.join(source) +"\n")
                    fout.write("- 下联: " + got + "\n\n")
                    fout.flush()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give test file path. First is the corpus path, and the second is out path.")
    test(sys.argv[1])


