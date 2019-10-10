import pickle
from DL.biLstm_Crf import LSTM_CRF
import tensorflow as tf

# 将句子转换为字序列
"""
def get_word(sentence):
    word_list = []
    sentence = ''.join(sentence.split(' '))
    for i in sentence:
        word_list.append(i)
    return word_list

def read_file(filename):
    content = []
    text = open(filename, 'r', encoding='utf-8')
    for eachline in text:
        eachline = eachline.strip('\n')
        eachline = eachline.strip(' ')
        word_list = get_word(eachline)
        content.append(word_list)
    return content
"""


def read_file(file_name):
    content = []
    f = open(file_name, 'r', encoding='utf-8')
    for line in f:
        content.append(line.strip().split())
    #print(content)
    return content


# def read_doc()


def sequence2id(doc):
    '''
    :param filename:
    :return: 将文字，转换为数字
    '''
    content2id = []

    # content = read_file(filename)
    content = doc.split()
    #print(content)
    with open('DL/data/word2id.pkl', 'rb') as fr:
        word = pickle.load(fr)
    w = []
    for key in content:
        if key.isdigit():
            key = '<NUM>'
        elif key not in word:
            key = '<UNK>'
        w.append(word[key])
    content2id.append(w)

    return content2id


def convert(sentence, label_line):
    # print(sentence)
    entities = []
    # words = word_tokenize(sentence)
    words = sentence.split()
    # print(words)

    label = [k.astype(str) for k in label_line]
    label.append('0')  # 防止最后一位不为0
    # print(label)
    # print(len(label))
    for word in words:
        # print(words.index(word))
        tag = label[words.index(word)]
        if tag != '0':
            # word_dict[word] = label2tag[tag.astype(int)]
            # print([word, label2tag[tag.astype(int)]])
            entities.append(word)
    # print('\n')
    return entities




def val(model, doc):
    session = tf.Session()
    session.run(tf.global_variables_initializer())
    save_path = tf.train.latest_checkpoint('DL/checkpoints/biLstm_crf_eng')
    saver = tf.train.Saver()
    saver.restore(sess=session, save_path=save_path)

    content = sequence2id(doc)
    # print(content)
    label = model.predict(session, content)
    #print(label)

    return label[0]


def get_named_enities(doc):
    named_entities = []

    model = LSTM_CRF()

    label = val(model, doc)

    #print(label)
    words = convert(doc, label)
    named_entities.append(words)

    return named_entities
    # print(sentences[i])
    # print(word_dict)