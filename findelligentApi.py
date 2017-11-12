#!/usr/bin/env python3

import argparse
import passageRetriever
import searching
import tokenizer

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
    query = tokenizer.tokenize_query(args.query)
    search = searching.Searching("/tmp/")
    search.index_write(simplePassageDict)
    search.query_write(query)
    search.score_density_distribution(args.windowsize, passage.get_passage_dictionary_size())
    for rank, i in enumerate(search.get_results()):
        print("Rank is: " + str(rank) + " Score is: " + str(i[1]) + " for document " + str(i[0]) + " with content " + str(simplePassageDict[i[0]]))

