#!/usr/bin/env python3

import argparse
import nltk
import string


class PassageParser:
    """ Transform plain text into hash table with passages and their vector of strings """

    def __init__(self, document):
        """ Constructor """
        self.doc = document

    def file_to_array(self):
        """ Transform text file into array of words without spaces """
        return [word for line in open(self.doc, 'r') for word in line.split()]

    def parse_dd(self, window_size):
        """ Generate passages by window, one passage by word """
        # TBD: Add window_size verification (even number)
        wordArray = self.file_to_array()
        passageList = {}
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
            passageList[index] = tempPassageList
        return passageList

    def tokenize_dd(self, docs_dictionary):
        """ Tokenize a list of lists of strings. Apply stemming and remove stop words without affecting list structure.  """
        stemmer = nltk.stem.PorterStemmer()
        translator = str.maketrans('', '', string.punctuation)
        for line, document in docs_dictionary.items():
            for index, word in enumerate(document):
                document[index] = stemmer.stem(word)
                document[index] = document[index].lower()
                document[index] = document[index].translate(translator)
            docs_dictionary[line] = document
        return docs_dictionary


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-w", "--windowsize",
                           help="Window size in number of words (even number)", type=int)
    argparser.add_argument(
        "-q", "--query", help="Query to be applied to the document", type=str)
    argparser.add_argument(
        "document", help="Document file as plain text to be ranked", type=str)
    args = argparser.parse_args()
    passage = PassageParser(args.document)
    passageList = passage.parse_dd(args.windowsize)
    print(passage.tokenize_dd(passageList))
