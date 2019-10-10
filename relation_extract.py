from ADV import find_ADV
from SPO import find_SVO, get_whole_noun, get_subs, get_objs, _is_non_aux_verb
from DL.predict import get_named_enities
import spacy
import contractions as ctr
import neuralcoref
from string import punctuation

nlp = spacy.load('en_core_web_md')
neuralcoref.add_to_pipe(nlp, greedy=1.0)


def remove_stopwords(doc):
    """
    this function will remove  some stopwords
    :param doc: string
    :return: string
    """
    stop_words = ['the', 'a', 'an', 'those', 'these', 'its', 'my', 'your', 'his', 'her', 'their']
    doc = doc.split()
    doc = [tok for tok in doc if tok.lower() not in stop_words]
    doc = " ".join(doc)
    return doc


def coreference_resolution(doc, entities):
    """
    compare every two words and change the threshold to -1,
    and juedge if the word that is going to be replaced is an entity that we need
    """

    BAN1 = ['its', '\'s', 'we', 'the', 'a', 'that']  # words can not be replaced
    BAN2 = ['it', 'he', 'she', 'her', 'its', 'him', 'I', 'you', 'your', 'yours', 'me', 'they', 'them',
            '']  # can not use these words to replace others

    s = str(doc)
    for i, nums in doc._.coref_scores.items():  # get all scores between every two words
        for word, n in nums.items():
            is_entity = False
            for w in entities:  # if the word is an entity we need
                if str(i).strip() in w:
                    is_entity = True
                    break
            if is_entity == False:
                if n > -1 and str(i) not in BAN1 and str(word) not in BAN2:
                    s = s.replace(str(i), str(word))

    return s


def doc_helper(doc):
    """
    this function do all preprocessing
    :param doc: an original text string
    :return: the string analyzed by spacy
    """
    doc = ctr.fix(doc)
    doc = nlp(doc)
    doc = doc._.coref_resolved
    doc = remove_stopwords(doc)
    doc = nlp(doc)
    return doc


def get_entites(doc):
    """
    get all entities
    :param doc: processed doc
    :return:  a list of entities
    """
    word_chunks = list(doc.noun_chunks)
    entities = []
    for x in doc.ents:
        for token in doc.noun_chunks:
            if x.text in token.text and token.root.pos_ != 'VERB':
                for token2 in doc.noun_chunks:
                    if str(token.root) in str(token2.root) and token.root.pos_ == token2.root.pos_:
                        entities.append(token2.root)
                    else:
                        entities.append(token.root)

    verb = [tok for tok in doc if _is_non_aux_verb(tok)]
    # get more entities
    for v in verb:
        subs = get_subs(v)
        for sub in subs:
            if sub in entities:
                entities.extend(subs)
        objs = get_objs(v)
        for obj in objs:
            if obj[-1] in entities:
                entities.extend([obj[-1] for obj in objs])
    named_entities = [get_whole_noun(entity, word_chunks) for entity in entities if entity.pos_ != 'VERB']

    # get entities from BiLSTM model
    new_entities = get_named_enities(str(doc))[0]
    for chunk in word_chunks:
        for ent in new_entities:
            if ent in chunk.text:
                named_entities.append(get_whole_noun(chunk.root, word_chunks))

    named_entities = list(set(named_entities))
    return named_entities


def get_ent_and_rel(doc):
    """
    get all EREs
    :param doc: an original text
    :return: a list of EREs
    """
    ERE = []
    ere = []
    entities = get_entites(doc)  # get entity first to optimize the coreference-resolution

    doc = coreference_resolution(doc, entities)
    doc = nlp(doc)

    SVO = find_SVO(doc)
    SVA = find_ADV(doc, SVO)

    for svo in SVO:
        if svo[0] in entities or svo[2] in entities:
            ere.append(svo)

    for sva in SVA:
        if sva[0] in entities or sva[2] in entities:
            ere.append(sva)

    for e in ere:
        if e not in ERE:
            ERE.append(e)
    ERE = filter_ERE(ERE)
    print(ERE)
    return ERE


def filter_ERE(ERE):
    """
    remove some EREs that are not correct
    :param ERE: list of EREs
    :return: list of EREs
    """
    BANE = ["’s", "'s", "am", "is", "are", "was", "were", " ", "–", "", ",", '”', "’"]
    BANR = ["’s", "'s", " ", ""]
    BANE.extend([i for i in punctuation])
    BANR.extend([i for i in punctuation])

    for ere in ERE:
        if ere[0] in BANE or ere[1] in BANR or ere[2] in BANE:
            ERE.remove(ere)
    return ERE


def ERE(doc):
    """
    combine all functions and get EREs
    """
    doc = doc_helper(doc)
    ERE = get_ent_and_rel(doc)
    return ERE
