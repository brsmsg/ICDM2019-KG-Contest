# -*-coding:Latin-1 -*
from SPO import find_SVO, get_whole_noun

noun = {'NOUN', 'PRON', 'PROPN'}

def find_ADV(sentence, SVO):
    """
    this fuchtion will get some relations of
    :param sentence: spacy analyzed text
    :param SVO: the SVO relation list
    :return: list of EREs
    """
    ADV = []
    word_chunks = list(sentence.noun_chunks)
    for token in sentence:
        _has_sub = False
        if token.dep_ == 'pobj' and token.head.text != 'of' and token.head.head.pos_ in noun:
            prep = token.head
            for svo in SVO:
                if get_whole_noun(token.head.head, word_chunks) in svo:
                    sva = [svo[0], str(prep), get_whole_noun(token, word_chunks)]
                    ADV.append(sva)
                    _has_sub = True
            if _has_sub == False:
                sva = [get_whole_noun(token.head.head, word_chunks), str(prep), get_whole_noun(token, word_chunks)]
                ADV.append(sva)
    return (ADV)


def SVA(sentence):
    """
    :param sentence: spacy analyzed text
    :return: list of EREs
    """
    SVO = find_SVO(sentence)
    ADV = find_ADV(sentence, SVO)
    return ADV

