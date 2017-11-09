#!/usr/bin/env python3

import argparse
import passageRetriever
import whoosh.fields
import whoosh.index
import whoosh.qparser
import whoosh.query
import whoosh.scoring
import math

# Custom Model


class DensityDistributions(whoosh.scoring.WeightingModel):
    """Implements the Density Distributions scoring algorithm.
    """

    def __init__(self, window, qf_dictionary):
        self.W = window
        self.qfDict = qf_dictionary

    def scorer(self, searcher, fieldname, text, qf):
        # print(text)
        # print(fieldname)
        qf = self.qfDict[text.decode("utf-8")]
        # print(qf)
        # FIXME qf is not working because the query is normalized I think. Ask the author of the library.
        # print(self.qfDict)
        # print(text)
        return DDScorer(searcher, fieldname, text, self.W, qf)


class DDScorer(whoosh.scoring.BaseScorer):

    def __init__(self, searcher, fieldname, text, window, qf):
        # print(text)
        # IDF and average field length are global statistics, so get them from
        # the top-level searcher
        parent = searcher.get_parent()  # Returns self if no parent
        self.idf = parent.idf(fieldname, text)
        self.W = window
        # self.setup(searcher, fieldname, text)
        self.qf = qf
        self.text = text
        # print(text)

    def score(self, matcher):
        # s = density_distribution(self.idf, self.W, self.qf, matcher)
        #print(matcher.value_as('positions'))
        finalScore = 0
        for position in matcher.value_as('positions'):
            x = position - (self.W / 2)
            hanning = 0.5 * (1 + math.cos(2 * math.pi * x / self.W))
            #print("Hanning de " + str(self.text) + " en posicion " + str(position) + " es " + str(hanning))
            weightQueryTerm = math.log(self.qf + 1, 2)
            #print("Weight de " + str(self.text) + " en posicion " + str(position) + " es " + str(weightQueryTerm))
            #print("IDF de " + str(self.text) + " en posicion " + str(position) + " es " + str(self.idf))
            finalScore = finalScore + (hanning * weightQueryTerm * self.idf)
            #print("Score de " + str(self.text) + " en posicion " + str(position) + " es " + str(finalScore))
        #print("Score for " + str(self.text) + "is " + str(finalScore))
        return finalScore


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-w", "--windowsize",
                           help="Window size in number of words (even number)", type=int)
    argparser.add_argument("-q", "--query",
                           help="Original query from user", type=str)
    argparser.add_argument(
        "document", help="Document file as plain text to be ranked", type=str)
    args = argparser.parse_args()
    passage = passageRetriever.PassageParser(args.document)
    passage.parse_docs_dd(args.windowsize)
    passage.tokenize_dd()
    simplePassageDict = passage.get_simplify_passage_dd(args.query)
    print(simplePassageDict)
    print(passage.get_passage_dictionary_size())
    schema = whoosh.fields.Schema(
        id=whoosh.fields.STORED, content=whoosh.fields.TEXT(stored=True))
    index = whoosh.index.create_in("/tmp/", schema)
    writer = index.writer()
    # for line, document in simplePassageDict.items():
    writer.add_document(
        id=1, content=['my', 'name', 'is', 'francisco', 'vargas'])
    writer.add_document(
        id=2, content=['francisco', 'is', 'an', 'electrical', 'engineer'])
    writer.add_document(
        id=3, content=['name', 'is', 'francisco', 'vargas', 'francisco'])
    writer.commit()
    # with index.searcher() as searcher:
    #     print(searcher.doc_count_all())
    #     print(searcher.document_number(content="francisco"))
    #     print(len(list(searcher.document_numbers(content="francisco"))))
    #     print(searcher.idf("content", "francisco"))
    queryList = ["francisco", "name"]
    query = whoosh.qparser.QueryParser(
        "content", index.schema, group=whoosh.qparser.OrGroup).parse(str(queryList))

    # print(query.all_terms())

    # for i in query.iter_all_terms():
    #     print(i[1])

    qfDict = dict()
    for i in queryList:
        qfDict[i] = qfDict.get(i, 0) + 1

    #print(qfDict)

    with index.searcher(weighting=DensityDistributions(4, qfDict)) as s:
        results = s.search(query)
        for result in results.items():
            print(result)
