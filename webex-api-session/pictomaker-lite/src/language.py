#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PictoLanguage
=============
This module tokenizes sentences via NLP
"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2022, mianfg"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "Creative Commons Zero v1.0 Universal"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "hello@mianfg.me"
__status__      = "Production"


import spacy, requests, json


SIMPLIFIER = {
    'ADJ' :     "ADJ",
    'ADP' :     "ADP",
    'ADV' :     "ADV",
    'AUX' :     "VERB",
    'CONJ' :    "CONJ",
    'CCONJ' :   "CONJ",
    'DET' :     "DET",
    'INTJ' :    "INTJ",
    'NOUN' :    "NOUN",
    'NUM' :     "NOUN",
    'PART' :    "OTHER",
    'PRON' :    "PRON",
    'PROPN' :   "NOUN",
    'PUNCT' :   "OTHER",
    'SCONJ' :   "CONJ",
    'SYM' :     "OTHER",
    'VERB' :    "VERB",
    'X' :       "OTHER",
    'SPACE' :   "OTHER"     # space -- note: tokenizer deletes this
}

IMPORTANCES = ['VERB', 'NOUN', 'ADJ', 'ADV', 'DET', 'PRON', 'INTJ', 'CONJ', 'ADP', 'OTHER']

class PictoLanguage:
    def __init__(self):
        self.__NLP = {
            'en': spacy.load("en_core_web_sm"),
            'es': spacy.load("es_core_news_sm"),
            'pl': spacy.load("pl_core_news_sm")
        }

    def pictograms(self, word, language):
        req = requests.get(f'https://api.arasaac.org/api/pictograms/{language}/bestsearch/{word}')
        return [pic['_id'] for pic in json.loads(req.text)]

    def tokenize(self, sentence, language):
        """
        Tokenizes sentence into an array of PictoWords:
        """

        # iterate over words
        nlp = self.__NLP[language](sentence)

        split = sentence.split()
        tokens = [{
            'text': token.text,
            'lemma': token.lemma_,
            'pos': SIMPLIFIER[token.pos_],
            'arasaac_ids': self.pictograms(token.lemma_, language)
        } for token in nlp]
        tokens_pos = []

        i = 0
        for token in tokens:
            if split[i] == token['text']:
                tokens_pos.append(i)
                i += 1
            elif split[i].startswith(token['text']):
                tokens_pos.append(i)
                split[i] = split[i][len(token['text']):]
            else:
                print(f"ERROR tokenizing sentence \"{sentence}\"")

        findall = lambda list, element: [i for i, x in enumerate(list) if x == element]
        return [{
          'text': text,
          'pos': sorted([tokens[j]['pos'] for j in findall(tokens_pos, i)],
            key=lambda el: IMPORTANCES.index(el))[0],
          'lemma': "".join([tokens[j]['lemma'] for j in findall(tokens_pos, i)]),
          'arasaac_ids': list(set().union(*[tokens[j]['arasaac_ids'] for j in findall(tokens_pos, i)]))
        } for i, text in enumerate(sentence.split())]
