# -*- coding:utf-8 -*-
class Parameters(object):

    num_epochs = 10
    vocab_size = 20002
    embedding_size = 200
    batch_size = 64
    hidden_dim = 128
    learning_rate = 0.001
    clip = 5.0
    lr = 0.5
    keep_pro = 0.7
    num_tags = 9


    train_data = 'data/eng.train'
    test_data = 'data/eng.testa'
    eva = 'data/eval'