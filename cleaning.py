"""
__file__

    cleaning.py.py

__description__

    This file provide function to clean the clean for nlp task

__author__

    Liang yongjie 

"""

from nltk.stem import WordNetLemmatizer,PorterStemmer

st = PorterStemmer()

def stem_tokens(tokens, stemmer=st):
    """

        Args:
            tokens (list) :
            stemmer (nltk stemmer) : nltk.stem.PorterStemmer()

        Returns:
            list: stem tokens

        Examples:

        import nltk
        english_stemmer = nltk.stem.PorterStemmer()
        stem_tokens(['apples'],english_stemmer)
        #['appl']
    """

    stemmed = []
    for token in tokens:
        stemmed.append(stemmer.stem(token))
    return stemmed


wl = WordNetLemmatizer()

def lement_tokens(tokens):
    stemmed = []
    for token in tokens:
        stemmed.append(wl.lemmatize(token))
    return stemmed
