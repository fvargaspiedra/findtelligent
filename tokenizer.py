"""Passage retriever for Findtelligent.

.. module::passageRetriever
   :synopsis: Passage Retriever module to generate and tokenize a list 
   of passages depending on the scoring method.

.. moduleauthor:: Francisco Vargas <fvargaspiedra@gmail.com>
"""

import argparse
import nltk


tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
stemmer = nltk.stem.PorterStemmer()


def tokenize_query(query):
    """ Tokenize a query """
    tokenized_query = tokenizer.tokenize(query)
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokenized_query = [
        word for word in tokenized_query if word not in stop_words]
    tokenized_query = [stemmer.stem(word) for word in tokenized_query]
    tokenized_query = [word.lower() for word in tokenized_query]
    return tokenized_query


def tokenize_doc_word(word):
    """ Tokenize a document's word (do not remove stop words) """
    tokenized_doc_word = tokenizer.tokenize(word)
    if len(tokenized_doc_word) > 0:
        tokenized_doc_word = tokenizer.tokenize(word)[0]
        tokenized_doc_word = stemmer.stem(tokenized_doc_word)
        tokenized_doc_word = tokenized_doc_word.lower()
    else:
        tokenized_doc_word = ""
    return tokenized_doc_word

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-q", "--query",
                           help="Original query from end user", type=str)
    args = argparser.parse_args()
    print(tokenize_query(args.query))
    print(tokenize_doc_word(".reading!!!!"))
