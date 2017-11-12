#!/usr/bin/env python3

import argparse
import passageRetriever
import searching
import tokenizer
import resultsParser

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-w", "--windowsize",
                           help="Window size in number of words (even number)", type=int)
    argparser.add_argument("-q", "--query",
                           help="Original query from user", type=str)
    argparser.add_argument("-u", "--url",
                           help="URL with the content", type=str)
    args = argparser.parse_args()
    
    passage = passageRetriever.PassageParser(args.document, args.windowsize)
    passage.parse_docs_dd()
    passage.tokenize_dd()
    simplePassageDict = passage.get_simplify_passage_dd(args.query)
    #print(passage.get_passage_dictionary())
    query = tokenizer.tokenize_query(args.query)
    search = searching.Searching("/tmp/")
    search.index_write(simplePassageDict)
    search.query_write(query)
    search.score_density_distribution(args.windowsize, passage.get_passage_dictionary_size())
    # for rank, i in enumerate(search.get_results()):
    #     print("Rank is: " + str(rank) + " Score is: " + str(i[1]) + " for document " + str(i[0]) + " with content " + passage.get_substring_from_file(i[0]))
    # #for i in search.get_results():
    resultsList = resultsParser.results_dd_max_percentage(search.get_results(), passage.get_passage_dictionary(), 60)
    for i in resultsList:
        print(passage.get_substring_from_file(i))
