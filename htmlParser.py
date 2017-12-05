"""HTML Parser for Findtelligent.

.. module::htmlParser
   :synopsis: HTML parser module to arrange HTML as needed for
   passage relevance analysis.

.. moduleauthor:: Francisco Vargas <fvargaspiedra@gmail.com>
.. todo::
    * Add a function to parse directly by receiving an HTML.
"""

import argparse
import urllib.request
import bs4


def html_to_text(url, dir):
    """Transform an HTML coming from a URL into a text document.

    :param url: URL of the HTML. The URL needs to be publicly reachable.
    :type dir: str.
    :param dir: Absolute path to store the parsed HTML.
    :type dir: str.
    :returns:  bool -- Always true.

    """
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    # Get rid of useless information
    for script in body(["script", "style", "title"]):
        script.extract()
    text = body.get_text()
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    with open(dir, 'w') as f:
        f.write(text)
    # TODO: Manage exceptions when something goes wrong
    return True


if __name__ == "__main__":
    # Dummy main to independent module testing
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-u", "--url",
                           help="URL with the content", type=str)
    args = argparser.parse_args()
    text = html_to_text(args.url)
    print(text)
