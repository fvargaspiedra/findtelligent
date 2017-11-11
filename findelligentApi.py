#!/usr/bin/env python3

import argparse
import passageRetriever
import searching

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
    tempDict = {101: ['my', 'name', 'is', 'francisco', 'vargas'], 220: ['francisco', 'different', 'different',
                                                                        'different', 'engineer'], 332: ['name', 'is', 'francisco', 'vargas', 'francisco']}
    queryList = ["francisco", "name", "different"]
    search = searching.Searching("/tmp/")
    search.index_write(tempDict)
    search.query_write(queryList)
    search.score_density_distribution(4, 3)
    print(search.get_results())
