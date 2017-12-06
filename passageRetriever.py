"""Passage retriever for Findtelligent.

.. module::passageRetriever
   :synopsis: Passage Retriever module to generate and tokenize a list 
   of passages depending on the scoring method.

.. moduleauthor:: Francisco Vargas <fvargaspiedra@gmail.com>
"""

import argparse
import nltk
import tokenizer
import re


class PassageParser(object):
    """Class to manage all the parsing process by passage.

    Each scoring method would require a different passage parsing. The
    general idea is to take a text document and create pseudo-documents
    by extracting passages using different techniques. 

    In this case a windows based technique is implemented for Density 
    Distribution, but this should be easily expandible to other techniques.

    Every function that ends with _dd sufix is specific for Density Distribution
    passage retrieval algorithm.

    """

    def __init__(self, document, window_size):
        """Construct a PassageParser object.

        :param document: Absolute path to text document to be parsed.
        :type document: str.
        :param window_size: Window size of passages to be parsed.
        :type window_size: int.

        """
        self.doc = document
        self.win_size = window_size
        # Empty dictionary of passages, the key will represent
        # a unique ID and the value the passage itself.
        self.passageDictionary = {}
        self.docArray = [word for line in open(
            self.doc, 'r') for word in line.split()]

    def parse_docs_dd(self):
        """Obtain pseudo-documents from text document.

        Divide a text document by passages based on a window size. For
        Density Distribution algorithm each word will represent a passage
        with a left and right window.

        This function will populate the attribute passageDictionary.

        """
        # TODO: Add window_size verification (even number)
        for index in range(0, len(self.docArray)):
            windowLeft = int(index - (self.win_size / 2))
            windowRight = int(index + (self.win_size / 2))
            tempPassageList = []
            for current in range(windowLeft, windowRight + 1):
                # Fill dictionary with empty strings when the position
                # is outside the document.
                if current < 0:
                    tempPassageList.append("")
                elif current > len(self.docArray) - 1:
                    tempPassageList.append("")
                else:
                    tempPassageList.append(self.docArray[current])
            self.passageDictionary[index] = [tempPassageList, 0.0]

    def tokenize_dd(self):
        """Tokenize the passage dictionary. """
        for line, document in self.passageDictionary.items():
            for index, word in enumerate(document[0]):
                document[0][index] = tokenizer.tokenize_doc_word(word)
            self.passageDictionary[line] = document

    def get_simplify_passage_dd(self, query):
        """Get a simplified version of the passage dictionary.
        
        This function returns only those passages that include
        a term that is part of the query and the passage.
        
        :param query: Query to get the relevant passages.
        :type query: str.
        :returns:  dictionary -- A passage dictionary of only the intersection between a passage and the query terms.

        """
        tokQuery = tokenizer.tokenize_query(query)
        tokQuery = set(tokQuery)
        tempPassageDictionary = {}
        for line, document in self.passageDictionary.items():
            documentSet = set(document[0])
            if bool(documentSet & tokQuery):
                tempPassageDictionary[line] = document
        return tempPassageDictionary

    def get_passage_dictionary(self):
        """Getter of passage dictionary.

        :returns:  dictionary -- The passage dictionary.

        """
        return self.passageDictionary

    def get_passage_dictionary_size(self):
        """Size of passage dictionary.

        :returns:  int -- Number of passages in the dictionary.

        """
        return len(self.passageDictionary)

    def get_substring_from_file(self, element_number):
        """Get a passage based on a word number.

        :param element_number: Number of the word.
        :type element_number: int.        
        :returns:  str -- The passage corresponding to the number of the word requested.

        """
        if (element_number - self.win_size / 2) < 0:
            return ' '.join(self.docArray[0:(element_number + int(self.win_size / 2))])
        else:
            return ' '.join(self.docArray[(element_number - int(self.win_size / 2)):(element_number + int(self.win_size / 2))])

    def get_substring_from_file_regex(self, element_number):
        """Get a passage based on a word number with RegEx form.

        :param element_number: Number of the word.
        :type element_number: int.        
        :returns:  str -- The passage in RegEx form corresponding to the number of the word requested.

        """
        if (element_number - self.win_size / 2) < 0:
            escapedList = (re.escape(i) for i in self.docArray[
                           0:(element_number + int(self.win_size / 2))])
            return '[^a-zA-Z0-9]*'.join(escapedList)
        else:
            escapedList = (re.escape(i) for i in self.docArray[
                           (element_number - int(self.win_size / 2)):(element_number + int(self.win_size / 2))])
            return '[^a-zA-Z0-9]*'.join(escapedList)

    def get_passages_from_list_regex(self, id_list):
        """Get a list of passages based on a list of word numbers (ids) with RegEx form.

        :param id_list: List of IDs (or word numbers).
        :type id_list: list.        
        :returns:  str -- A list of passages in RegEx form corresponding to the list of ids requested.

        """
        passagesList = []
        for i in id_list:
            tempDict = {
                'id': i, 'regexp': self.get_substring_from_file_regex(i)}
            passagesList.append(tempDict)
        return passagesList

if __name__ == "__main__":
    # Dummy main to test the modile independently
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
