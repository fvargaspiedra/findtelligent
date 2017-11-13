#!/usr/bin/env python3

import argparse
import urllib.request
import bs4

def html_to_text(url, dir):
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    for script in body(["script", "style", "title"]):
        script.extract()
    text = body.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    with open(dir, 'w') as f: 
        f.write(text) 
    return True


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-u", "--url",
                           help="URL with the content", type=str)
    args = argparser.parse_args()
    text = html_to_text(args.url)
    print(text)