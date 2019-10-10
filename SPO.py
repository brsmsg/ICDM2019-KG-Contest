SUBJECTS = {"nsubj", "nsubjpass", "agent"}
MODIFIER = {"amod", "nmod", "compound", "pobj", "subtok", "nummod", "poss", "case"}
BANDEP = {"cc", "nummod", "prep"}
TEXT = {'of', 'x', '-'}  # some import texts that can not be removed
NFV = {"advcl", "xcomp", "conj", "ccomp"}  # none-finite verb
DIROBJ = {'dobj', 'attr'}
BANVERB = {'Be'}


def get_chunk(word, chunks):
    """
    get chunks of the word
    """
    for chunk in chunks:
        if chunk.root == word:
            return chunk
    return word


def is_passive(verb):
    """
    judge if the verb is passive form
    """
    lefts = verb.lefts
    for word in lefts:
        if word.dep_ == 'auxpass':
            return True
    return False


def _is_non_aux_verb(tok):
    """
    judge if the verb is a normal verb we want
    """
    return tok.pos_ == "VERB" and (tok.dep_ != "aux" and tok.dep_ != "auxpass" and tok.text not in BANVERB)


# def judgr_sentence_passive(sentence):
#
#     for token in sentence:
#         if token.dep_ == 'auxpass':
#             return True
#     return False


def has_no_dir_sub(v):
    """
    judge if the verb which is not predicate has a direct subject
    """
    lefts = list(v.lefts)
    for w in lefts:
        if w.dep_ in SUBJECTS:
            return False
    return True


def get_whole_verb(v):
    """
    get the whole verb: e.g. 'look' -> 'look at'
    """
    for word in list(v.rights):
        if word.dep_ == 'prep':
            return str(v) + " " + word.text
    return v.text


def get_subs(v):
    """
    get all subjects of the verb
    :param v: verb
    :return: a subject list
    """
    subs = []
    if is_passive(v):
        rights = list(v.rights)
        for word in rights:
            if word.dep_ == 'prep':
                for w in list(word.rights):
                    if w.dep_ == 'pobj':
                        subs.append(w)
                        subs.extend(get_all_subs(subs))

    else:
        lefts = list(v.lefts)
        for word in lefts:
            if word.dep_ == 'nsubj':
                subs.append(word)
                subs.extend(get_all_subs(subs))
    return subs


def get_all_subs(subs):  # more than one subject
    """
    if the verb has more than one subjects, which may be connected with 'and', we can find them in this function
    :param subs: subject list
    :return: subject list with more subjects
    """
    more_subs = []
    for sub in subs:
        rights = list(sub.rights)
        for word in rights:
            if word.dep_ == 'conj':
                more_subs.append(word)
                more_subs.extend(get_all_subs(more_subs))
    return more_subs


def get_objs(v):
    """
    get all objects of the verb
    :param v: verb
    :return: an object list
    """
    objs = []
    prep_objs = []

    def rule(objs, prep_objs):
        if word.dep_ == 'dobj':
            objs.append([word])
            objs.extend(get_all_objs(objs))
        elif word.dep_ == 'prep':
            for w in list(word.rights):
                if w.dep_ == 'pobj':
                    prep_objs.append([word, w])
                    prep_objs.extend(get_all_objs(prep_objs))
                if w.dep_ == 'amod':
                    prep_objs.append([word, w])
                    prep_objs.extend(get_all_objs(prep_objs))
        if word.dep_ == 'acomp':  # 形容词 adj ‘dep’==acomp
            objs.append([word])
        if word.dep_ == "agent":  # 大多是  by xxx
            for x in word.rights:
                if x.dep_ == "pobj":
                    prep_objs.append([word, x])
                    prep_objs.extend(get_all_objs(prep_objs))
        if (word.dep_ == "conj" or word.dep_ == "ccomp" or word.dep_ == "xcomp") and word.pos_ != "VERB":
            for x in word.rights:
                if x.dep_ == "dobj":
                    objs.append([x])
                    objs.extend(get_all_objs(objs))
        if word.dep_ in DIROBJ:  # verb + obj
            objs.append([word])
            objs.extend(get_all_objs(objs))

    if is_passive(v):
        lefts = list(v.lefts)
        for word in lefts:
            if word.dep_ == 'nsubjpass':
                objs.append([word])
                objs.extend(get_all_objs(objs))
            rule(objs, prep_objs)
    else:
        rights = list(v.rights)
        for word in rights:
            rule(objs, prep_objs)
        lefts = list(v.lefts)
        for word in lefts:
            rule(objs, prep_objs)
    objs.extend(prep_objs)
    return objs


def have_example(word):
    """
    judge if there is some examples that could be entities
    """
    if word.text == 'as' and len(list(word.lefts)) > 0 and list(word.lefts)[0].text == 'such':
        return True
    return False


def get_all_objs(objs):  # more than one object
    """
    if the verb has more than one objects, which may be connected with 'and', we can find them in this function
    :param subs: object list
    :return: object list with more objects
    """
    more_objs = []
    if len(objs) == 0 or len(objs) >= 10:
        return more_objs
    for obj in objs:
        if len(obj) == 2:
            rights = list(obj[1].rights)
            if len(rights) == 0:
                return more_objs
            for word in rights:
                if word.dep_ == 'conj' or 'appose' and word.dep_ not in BANDEP:
                    more_objs.append([obj[0], word])  # obj[0] is prep
                    more_objs.extend(get_all_objs(more_objs))
                if have_example(word):
                    for w in list(word.rights):
                        if w.dep_ == 'pobj':
                            more_objs.append([obj[0], w])
                            more_objs.extend(get_all_objs(more_objs))
        else:
            rights = list(obj[0].rights)
            if len(rights) == 0:
                return more_objs
            for word in rights:
                if word.dep_ == 'conj' or 'appose' and word.dep_ not in BANDEP:
                    more_objs.append([word])
                    more_objs.extend(get_all_objs(more_objs))
                if have_example(word):
                    for w in list(word.rights):
                        if w.dep_ == 'pobj':
                            more_objs.append([w])
                            more_objs.extend(get_all_objs(more_objs))

    return more_objs


def find_SVO(sentence):
    """
    this function can extract relations from subject-predicate-object
    :param sentence: spacy analyzed text
    :return: an ERE list of SVO relations
    """
    PRON = {"he", "who", "which", "that", "I", "you", "she", "we", "they", "this", "these", "those"}
    word_chunks = list(sentence.noun_chunks)
    SVO = []
    verb = [tok for tok in sentence if _is_non_aux_verb(tok)]

    for v in verb:
        if v.dep_ in NFV and v.head.pos_ == 'VERB' and has_no_dir_sub(v):
            if v.head.text == 'Be' and v.text != 'Be':
                s = get_objs(v.head)
                subs = [tok[-1] for tok in s]
                objs = get_objs(v)
            else:
                subs = get_subs(v.head)
                objs = get_objs(v)

        else:
            subs = get_subs(v)
            objs = get_objs(v)
        for sub in subs:
            for obj in objs:
                if len(obj) == 1:
                    svo = [str(get_whole_noun(sub, word_chunks)), str(v), str(get_whole_noun(obj[0], word_chunks))]
                    if svo[0] != svo[2] and svo[0].lower() not in PRON and svo[2].lower() not in PRON:
                        SVO.append(svo)

                if len(obj) == 2:
                    svo = [str(get_whole_noun(sub, word_chunks)), get_whole_verb(v),
                           str(get_whole_noun(obj[1], word_chunks))]
                    if svo[0] != svo[2] and svo[0].lower() not in PRON and svo[2].lower() not in PRON:
                        SVO.append(svo)

    return SVO


def get_whole_noun(word, chunks):
    """
    return word_chunks
    """
    return str(get_chunk(word, chunks))






