"""Findtelligent API definition.

Core module to connect all the pieces together and expose the code using an API.

.. moduleauthor:: Francisco Vargas <fvargaspiedra@gmail.com>
"""

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
    """Get most relevant passages based on URL, query, and scoring function.

    API to extract the most relevant passages of the HTML based on the URL,
    a query, and the scoring function. The URL, the query, and the scoring
    method come on the query string.

    :returns: response -- HTTP response with JSON of relevant passages.

    """
    q = flask.request.args.get('q')
    url = flask.request.args.get('url')
    method = flask.request.args.get('method')
    htmlParser.html_to_text(url, "/tmp/findtelligent.html")
    results = evaluate_html("/tmp/findtelligent.html", q, method)
    if results:
        response = flask.make_response(flask.jsonify(results), 200)
        response.headers["Cache-Control"] = "max-age=300"
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    else:
        flask.abort(404)


def evaluate_html(dir, query, method):
    """Get most relevant passages from text based on query and scoring method.

    :param dir: Absolute path to text document.
    :type dir: str.
    :param query: Query to find the most relevant passages.
    :type query: str.
    :param method: Scoring method to be used.
    :type method: str.
    :returns:  list -- List of relevant passages.

    """
    if method == "dd":
        # Parse the text document for Density Distribution method
        # Window size value must be defined empirically
        window = 10
        passage = passageRetriever.PassageParser(dir, window)
        passage.parse_docs_dd()
        passage.tokenize_dd()
        simplePassageDict = passage.get_simplify_passage_dd(query)
        # Parse the query
        q = tokenizer.tokenize_query(query)
        # Create an index and score using Density Distribution algorithm
        search = searching.Searching("/tmp/")
        search.index_write(simplePassageDict)
        search.query_write(q)
        search.score_density_distribution(
            window, passage.get_passage_dictionary_size())
        # Parse the results based on percentile top scores
        percentile = 60
        resultsList = resultsParser.results_dd_max_percentage(
            search.get_results(), passage.get_passage_dictionary(), percentile)
        # Return the definitive list of relevant passages with RegEx format
        return passage.get_passages_from_list_regex(resultsList)
    else:
        return []

if __name__ == "__main__":
    # Dummy main to run Flask in debug mode by default
    app.run(debug=True)
