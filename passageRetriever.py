#!/usr/bin/env python3

import argparse
import nltk
import tokenizer


class PassageParser:
    """ Transform plain text into hash table with passages and their vector of strings """

    def __init__(self, document):
        """ Constructor """
        self.doc = document
        self.passageDictionary = {}

    def file_to_array(self):
        """ Transform text file into array of words without spaces """
        return [word for line in open(self.doc, 'r') for word in line.split()]

    def parse_docs_dd(self, window_size):
        """ Generate passages by window, one passage by word """
        # TBD: Add window_size verification (even number)
        wordArray = self.file_to_array()
        for index in range(0, len(wordArray)):
            windowLeft = int(index - (window_size / 2))
            windowRight = int(index + (window_size / 2))
            tempPassageList = []
            for current in range(windowLeft, windowRight + 1):
                if current < 0:
                    tempPassageList.append("")
                elif current > len(wordArray) - 1:
                    tempPassageList.append("")
                else:
                    tempPassageList.append(wordArray[current])
            self.passageDictionary[index] = tempPassageList

    def tokenize_dd(self):
        """ Tokenize a list of lists of strings. Apply stemming and remove stop words without affecting list structure.  """
        for line, document in self.passageDictionary.items():
            for index, word in enumerate(document):
                document[index] = tokenizer.tokenize_doc_word(word)
            self.passageDictionary[line] = document

    def get_simplify_passage_dd(self, query):
        tokQuery = tokenizer.tokenize_query(query)
        tokQuery = set(tokQuery)
        tempPassageDictionary = {}
        for line, document in self.passageDictionary.items():
            documentSet = set(document)
            if bool(documentSet & tokQuery):
                tempPassageDictionary[line] = document
        return tempPassageDictionary

    def get_passage_dictionary(self):
        return self.passageDictionary

    def get_passage_dictionary_size(self):
        return len(self.passageDictionary)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-w", "--windowsize",
                           help="Window size in number of words (even number)", type=int)
    argparser.add_argument("-q", "--query",
                           help="Original query from user", type=str)
    argparser.add_argument(
        "document", help="Document file as plain text to be ranked", type=str)
    args = argparser.parse_args()
    passage = PassageParser(args.document)
    passage.parse_docs_dd(args.windowsize)
    passage.tokenize_dd()
    print(passage.get_simplify_passage_dd(args.query))
