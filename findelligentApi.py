#!/usr/bin/env python3

import argparse
import passageRetriever
import searching
import tokenizer
import resultsParser
import htmlParser
import flask

app = flask.Flask(__name__)

@app.route("/api/v1/getbyurl", methods=["GET"])
def get_by_url():
    q = flask.request.args.get('q')
    url = flask.request.args.get('url')
    method = flask.request.args.get('method')
    htmlParser.html_to_text(url, "/tmp/findtelligent.html")
    return flask.jsonify(evaluate_html("/tmp/findtelligent.html", q, method))

def evaluate_html(dir, query, method):
    if method == "dd":
        window = 10
        passage = passageRetriever.PassageParser(dir, window)
        passage.parse_docs_dd()
        passage.tokenize_dd()
        simplePassageDict = passage.get_simplify_passage_dd(query)
        q = tokenizer.tokenize_query(query)
        search = searching.Searching("/tmp/")
        search.index_write(simplePassageDict)
        search.query_write(q)
        search.score_density_distribution(window, passage.get_passage_dictionary_size())
        resultsList = resultsParser.results_dd_max_percentage(search.get_results(), passage.get_passage_dictionary(), 60)
        return passage.get_passages_from_list_regex(resultsList)
    else:
        return []

if __name__ == "__main__":
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument("-w", "--windowsize",
    #                        help="Window size in number of words (even number)", type=int)
    # argparser.add_argument("-q", "--query",
    #                        help="Original query from user", type=str)
    # argparser.add_argument("-u", "--url",
    #                        help="URL with the content", type=str)
    # args = argparser.parse_args()
    # htmlParser.html_to_text(args.url, "/tmp/findtelligent.html")
    # passage = passageRetriever.PassageParser("/tmp/findtelligent.html", args.windowsize)
    # passage.parse_docs_dd()
    # passage.tokenize_dd()
    # simplePassageDict = passage.get_simplify_passage_dd(args.query)
    # query = tokenizer.tokenize_query(args.query)
    # search = searching.Searching("/tmp/")
    # search.index_write(simplePassageDict)
    # search.query_write(query)
    # search.score_density_distribution(args.windowsize, passage.get_passage_dictionary_size())
    # resultsList = resultsParser.results_dd_max_percentage(search.get_results(), passage.get_passage_dictionary(), 60)
    # print(passage.get_passages_from_list_regex(resultsList))
    app.run(debug=True)