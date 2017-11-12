#!/usr/bin/env python3

import whoosh.fields
import whoosh.index
import whoosh.qparser
import whoosh.query
import whoosh.scoring
import math
import numpy


class DensityDistributions(whoosh.scoring.WeightingModel):
    """Implements the Density Distributions scoring algorithm.
    """

    def __init__(self, window, doc_count, qf_dictionary):
        self.W = window
        self.qfDict = qf_dictionary
        self.dc = doc_count

    def scorer(self, searcher, fieldname, text, qf):
        qf = self.qfDict[text.decode("utf-8")]
        # FIXME qf is not working because the query is normalized I think. Ask
        # the author of the library.
        return DDScorer(searcher, fieldname, text, self.W, self.dc, qf)


class DDScorer(whoosh.scoring.BaseScorer):

    def __init__(self, searcher, fieldname, text, window, doc_count, qf):
        # IDF and average field length are global statistics, so get them from
        # the top-level searcher
        parent = searcher.get_parent()  # Returns self if no parent
        docFrequency = parent.doc_frequency(fieldname, text)
        self.idf = math.log(((doc_count + 1) / (docFrequency)), 2)
        self.W = window
        self.qf = qf
        #self.text = text

    def score(self, matcher):
        # print(matcher.value_as('positions'))
        finalScore = 0
        for position in matcher.value_as('positions'):
            x = position - (self.W / 2)
            hanning = 0.5 * (1 + math.cos(2 * math.pi * x / self.W))
            #print("Hanning de " + str(self.text) + " en posicion " + str(position) + " es " + str(hanning))
            weightQueryTerm = math.log(self.qf + 1, 2)
            #print("Weight de " + str(self.text) + " en posicion " + str(position) + " es " + str(weightQueryTerm))
            #print("IDF de " + str(self.text) + " en posicion " + str(position) + " es " + str(self.idf))
            finalScore = finalScore + (hanning * weightQueryTerm * self.idf)
        return finalScore


class Searching:

    def __init__(self, dir):
        self.schema = whoosh.fields.Schema(
            id=whoosh.fields.STORED, content=whoosh.fields.TEXT(stored=True))
        self.index = whoosh.index.create_in(dir, self.schema)
        self.query = whoosh.qparser.QueryParser(
            "content", self.index.schema, group=whoosh.qparser.OrGroup)
        self.query_freq_dictionary = {}
        self.results_list = []

    def index_write(self, collection_dictionary):
        writer = self.index.writer()
        for lineNum, document in collection_dictionary.items():
            writer.add_document(id=lineNum, content=document[0])
        writer.commit()

    def query_write(self, query_list):
        self.query = self.query.parse(' '.join(query_list))
        for i in query_list:
            self.query_freq_dictionary[
                i] = self.query_freq_dictionary.get(i, 0) + 1

    def score_density_distribution(self, window, doc_count):
        with self.index.searcher(weighting=DensityDistributions(window, doc_count, self.query_freq_dictionary)) as s:
            results = s.search(self.query, limit = None)
            for i, score in enumerate(results.items()):
                self.results_list.append([results.fields(i)['id'], score[1]])

    def get_results_top(self, top = -1):
        if top == -1:  
            return self.results_list
        elif top >= 1:
            return self.results_list[0:top]
        else:
            #FIXME add error for invalid top value
            pass

    def get_results(self):
        return self.results_list

    # def get_results_percentile(self, percentile):
    #     scoreList = []
    #     for i in self.results_list:
    #         scoreList.append(i[1])
    #     scoreArray = numpy.array(scoreList)
    #     perc = numpy.percentile(scoreArray, percentile)
    #     results_list_percentile = []
    #     for i in self.results_list:
    #         if i[1] >= perc:
    #             results_list_percentile.append(i)
    #     return results_list_percentile

