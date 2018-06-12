import tensorflow as tf
import numpy as np

# preprocessed data
from datasets.twitter import data
import data_utils

import seq2seq_wrapper
import importlib

import string
class chatbot:
    def __init__(self,train=False):
        # load data from pickle and npy files
        self.metadata, idx_q, idx_a = data.load_data(PATH='datasets/twitter/')
        (trainX, trainY), (testX, testY), (validX, validY) = data_utils.split_dataset(idx_q, idx_a)# parameters
        xseq_len = trainX.shape[-1]
        yseq_len = trainY.shape[-1]
        batch_size = 16
        xvocab_size = len(self.metadata['idx2w'])
        yvocab_size = xvocab_size
        emb_dim = 1024
        importlib.reload(seq2seq_wrapper)
        self.model = seq2seq_wrapper.Seq2Seq(xseq_len=xseq_len,
                                   yseq_len=yseq_len,
                                   xvocab_size=xvocab_size,
                                   yvocab_size=yvocab_size,
                                   ckpt_path='ckpt/twitter/',
                                   emb_dim=emb_dim,
                                   num_layers=3
                                   )
        if train:
            val_batch_gen = data_utils.rand_batch_gen(validX, validY, 32)
            train_batch_gen = data_utils.rand_batch_gen(trainX, trainY, batch_size)
            sess = self.model.train(train_batch_gen, val_batch_gen)
        self.sess = self.model.restore_last_session()

    def response(self,sentence):
        return self._vectorstring(self.model.predict(self.sess,self._stringtovec(sentence,20)))

    def _stringtovec(self,sentence,length):
        translator = str.maketrans('', '', string.punctuation)
        s = [int(self.metadata["w2idx"][e]) if e in self.metadata['idx2w'] else 1 for e in sentence.translate(translator).lower().split()]
        if len(s)<length:
            s+=[0]*(length-len(s))
        else:
            s=s[:length]
        return np.array(s).reshape((length,1))

    def _vectorstring(self,vec):
        s = ""
        for e in vec.flatten():
            if e != 0:
                s+=self.metadata["idx2w"][e]+" "
        return s
