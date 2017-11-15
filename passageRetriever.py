#!/usr/bin/env python3

import argparse
import nltk
import tokenizer


class PassageParser:
    """ Transform plain text into hash table with passages and their vector of strings """

    def __init__(self, document, window_size):
        """ Constructor """
        self.doc = document
        self.passageDictionary = {}
        self.win_size = window_size
        self.docArray = [word for line in open(self.doc, 'r') for word in line.split()]

    def parse_docs_dd(self):
        """ Generate passages by window, one passage by word """
        # TBD: Add window_size verification (even number)
        for index in range(0, len(self.docArray)):
            windowLeft = int(index - (self.win_size / 2))
            windowRight = int(index + (self.win_size / 2))
            tempPassageList = []
            for current in range(windowLeft, windowRight + 1):
                if current < 0:
                    tempPassageList.append("")
                elif current > len(self.docArray) - 1:
                    tempPassageList.append("")
                else:
                    tempPassageList.append(self.docArray[current])
            self.passageDictionary[index] = [tempPassageList, 0.0]

    def tokenize_dd(self):
        """ Tokenize a list of lists of strings. Apply stemming and remove stop words without affecting list structure.  """
        for line, document in self.passageDictionary.items():
            for index, word in enumerate(document[0]):
                document[0][index] = tokenizer.tokenize_doc_word(word)
            self.passageDictionary[line] = document

    def get_simplify_passage_dd(self, query):
        tokQuery = tokenizer.tokenize_query(query)
        tokQuery = set(tokQuery)
        tempPassageDictionary = {}
        for line, document in self.passageDictionary.items():
            documentSet = set(document[0])
            if bool(documentSet & tokQuery):
                tempPassageDictionary[line] = document
        return tempPassageDictionary

    def get_passage_dictionary(self):
        return self.passageDictionary

    def get_passage_dictionary_size(self):
        return len(self.passageDictionary)

    def get_substring_from_file(self, element_number):
        if (element_number - self.win_size / 2) < 0:
            return ' '.join(self.docArray[0:(element_number + int(self.win_size / 2))])
        else:
            return ' '.join(self.docArray[(element_number - int(self.win_size / 2)):(element_number + int(self.win_size / 2))])

    def get_substring_from_file_regex(self, element_number):
        if (element_number - self.win_size / 2) < 0:
            return '[^a-zA-Z0-9]*'.join(self.docArray[0:(element_number + int(self.win_size / 2))])
        else:
            return '[^a-zA-Z0-9]*'.join(self.docArray[(element_number - int(self.win_size / 2)):(element_number + int(self.win_size / 2))])

    def get_passages_from_list_regex(self, id_list):
        passagesList = []
        for i in id_list:
            tempDict = { 'id': i, 'regexp': self.get_substring_from_file_regex(i)}
            #passagesDict["id"] = self.get_substring_from_file_regex(i)
            #passagesDict[i] = self.get_substring_from_file_regex(i)
            passagesList.append(tempDict)
        return passagesList

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
