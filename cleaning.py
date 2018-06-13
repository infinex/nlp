"""
__file__

    cleaning.py.py

__description__

    This file provide function to clean the clean for nlp task

__author__

    Liang yongjie 

"""

from nltk.stem import WordNetLemmatizer

def stem_tokens(tokens, stemmer):
    """
        Args:
            tokens (list)
            stemmer (nltk stemmer)

        Returns:
            list: stem tokens
    """

    stemmed = []
    for token in tokens:
        stemmed.append(stemmer.stem(token))
    return stemmed


st = WordNetLemmatizer()

def lement_tokens(tokens):
    stemmed = []
    for token in tokens:
        stemmed.append(st.lemmatize(token))
    return stemmed
