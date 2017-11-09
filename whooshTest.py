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
        #print(fieldname)
        qf = self.qfDict[text.decode("utf-8")]
        # print(qf)
        #FIXME qf is not working because the query is normalized I think. Ask the author of the library.
        #print(self.qfDict)
        return DDScorer(searcher, fieldname, text, self.W, qf)


class DDScorer(whoosh.scoring.BaseScorer):

    def __init__(self, searcher, fieldname, text, window, qf):
        #print(text)
        # IDF and average field length are global statistics, so get them from
        # the top-level searcher
        # parent = searcher.get_parent()  # Returns self if no parent
        #self.idf = parent.idf(fieldname, text)
        self.W = window
        # self.setup(searcher, fieldname, text)
        self.qf = qf

    def score(self, matcher):
        # s = density_distribution(self.idf, self.W, self.qf, matcher)
        #print(matcher.value_as('positions'))
        # print(self.W)
        # print(self.qf)
        return self.qf


def pos_score_fn(searcher, fieldname, text, matcher):
    # print(text)
    # print(fieldname)
    # print(matcher.value_as('positions'))
    # for i in matcher.matching_terms(id=None):
    #     print(i)
    print(matcher.items_as(id))
    return 1.0

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
        id=1, content=['summari', 'should', 'francisco', 'nothing', 'readabl'])
    writer.add_document(
        id=2, content=['francisco', 'vargas', 'piedra', 'isabelle', 'guapa'])
    writer.add_document(
        id=3, content=['francisco', 'francisco', 'piedra', 'isabelle', 'guapa'])
    writer.add_document(
        id=4, content=['francisco', 'francisco', 'human', 'human', 'readabl'])
    writer.add_document(
        id=5, content=['summari', 'should', 'be', 'francisco', 'readabl'])
    writer.add_document(
        id=6, content=['francisco', 'vargas', 'francisco', 'francisco', 'guapa'])
    writer.commit()
    # with index.searcher() as searcher:
    #     print(searcher.doc_count_all())
    #     print(searcher.document_number(content="francisco"))
    #     print(len(list(searcher.document_numbers(content="francisco"))))
    #     print(searcher.idf("content", "francisco"))
    queryList = ["human", "francisco", "human", "human", "human"]
    query = whoosh.qparser.QueryParser(
        "content", index.schema, group=whoosh.qparser.OrGroup).parse(str(queryList))

    # print(query.all_terms())

    # for i in query.iter_all_terms():
    #     print(i[1])

    qfDict = dict()
    for i in queryList:
        qfDict[i] = qfDict.get(i, 0) + 1

    print(qfDict)

    with index.searcher(weighting=DensityDistributions(4, qfDict)) as s:
        results = s.search(query)
        for result in results.items():
            print(result)
