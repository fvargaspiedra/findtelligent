"""Indexing and scoring for Findtelligent.

.. module::searching
   :synopsis: Indexing and scoring module to index in real time and 
   apply a custom scoring function. By the moment only Density Distribution
   scoring function is available.

.. moduleauthor:: Francisco Vargas <fvargaspiedra@gmail.com>
"""

import whoosh.fields
import whoosh.index
import whoosh.qparser
import whoosh.query
import whoosh.scoring
import math
import numpy


class DensityDistributions(whoosh.scoring.WeightingModel):
    """Implement the Density Distributions scoring algorithm.

    This class is automatically called by Whoosh during scoring phase.

    """
    def __init__(self, window, doc_count, qf_dictionary):
        """Construct a DensityDistributions object.

        :param window: Window size used to build the passages.
        :type window: int.
        :param doc_count: number of passages.
        :type doc_count: int.
        :param qf_dictionary: dictionary of query frequency (number of terms by word).
        :type qf_dictionary: dictionary.

        """
        self.W = window
        self.qfDict = qf_dictionary
        self.dc = doc_count

    def scorer(self, searcher, fieldname, text, qf):
        """Calculate density distribution by calling a DD scorer.

        The parameters are standard objects from Whoosh.

        """
        # TODO: QF should be automatically filled by Whoosh but is not working.
        # That's why is passed manually.
        qf = self.qfDict[text.decode("utf-8")]
        return DDScorer(searcher, fieldname, text, self.W, self.dc, qf)


class DDScorer(whoosh.scoring.BaseScorer):
    """Implement the Density Distributions scoring algorithm.

    This class is automatically called by Whoosh during scoring phase.

    """
    def __init__(self, searcher, fieldname, text, window, doc_count, qf):
        """Construct necessary elements to score.

        Only window, doc_count and qf are manually passed the rest of attributes
        are standard Whoosh objects.

        """
        # IDF and average field length are global statistics, so get them from
        # the top-level searcher
        parent = searcher.get_parent()
        docFrequency = parent.doc_frequency(fieldname, text)
        self.idf = math.log(((doc_count + 1) / (docFrequency)), 2)
        self.W = window
        self.qf = qf

    def score(self, matcher):
        finalScore = 0
        for position in matcher.value_as('positions'):
            x = position - (self.W / 2)
            hanning = 0.5 * (1 + math.cos(2 * math.pi * x / self.W))
            weightQueryTerm = math.log(self.qf + 1, 2)
            finalScore = finalScore + (hanning * weightQueryTerm * self.idf)
        return finalScore


class Searching(object):
    """Indexing and scoring class.

    By the moment only Density Distribution is implemented, but this should be easily
    scalable to other methods.

    """
    def __init__(self, dir):
        """Construct a Searching object.

        :param dir: Path to store the index created.
        :type dir: str.

        """
        # Define schema
        self.schema = whoosh.fields.Schema(
            id=whoosh.fields.STORED, content=whoosh.fields.TEXT(stored=True))
        # Create index to be populated
        self.index = whoosh.index.create_in(dir, self.schema)
        # Define query parser based on schema
        self.query = whoosh.qparser.QueryParser(
            "content", self.index.schema, group=whoosh.qparser.OrGroup)
        self.query_freq_dictionary = {}
        self.results_list = []

    def index_write(self, collection_dictionary):
        """Write to the index based on collection of passages.

        :param collection_dictionary: Dictionary of IDs as keys and passages as values.
        :type collection_dictionary: dictionary.

        """
        writer = self.index.writer()
        for lineNum, document in collection_dictionary.items():
            writer.add_document(id=lineNum, content=document[0])
        writer.commit()

    def query_write(self, query_list):
        """Write the query and calculate QF.

        :param query_list: A list that contains each term of the query.
        :type query_list: list.

        """
        self.query = self.query.parse(' '.join(query_list))
        for i in query_list:
            self.query_freq_dictionary[
                i] = self.query_freq_dictionary.get(i, 0) + 1

    def score_density_distribution(self, window, doc_count):
        """Calculate density distribution.

        :param window: Window used to build the passage.
        :type window: int.
        :param doc_count: number of documents.
        :type doc_count: int.

        """
        with self.index.searcher(weighting=DensityDistributions(window, doc_count, self.query_freq_dictionary)) as s:
            results = s.search(self.query, limit=None)
            for i, score in enumerate(results.items()):
                self.results_list.append([results.fields(i)['id'], score[1]])

    def get_results_top(self, top=-1):
        """Return the top N scores.

        :param top: top N scores desired. If not defined all the values are returned
        :type top: int.

        """   
        if top == -1:
            return self.results_list
        elif top >= 1:
            return self.results_list[0:top]
        else:
            # TODO: add error for invalid top value
            pass

    def get_results(self):
        """Return all the scores."""  
        return self.results_list
