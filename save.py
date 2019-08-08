import os
import re
from collections import namedtuple
from datetime import datetime
from pathlib import Path

import requests
from lxml import etree as ET
from lxml.builder import E
from lxml.html import tostring
from readability import Document

TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S"
ROOT_DIRECTORY = os.getenv("LINKBOX_HOME")

HtmlArticle = namedtuple("HtmlArticle", ["title", "content", "url"])


def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'

    https://github.com/django/django/blob/1af469e67fd3928a4b01722d4706c066000014e9/django/utils/text.py#L221-L231
    """
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


def filepath(title, timestamp):
    filename = get_valid_filename(timestamp.strftime(TIMESTAMP_FORMAT) + " " + title)
    p = Path(ROOT_DIRECTORY) / "unread" / (filename + ".html")
    return p


def save(html, filepath):
    os.makedirs(Path(ROOT_DIRECTORY) / "unread", exist_ok=True)
    with open(filepath, "w") as f:
        f.write(html)


def extract_article(html, url):
    doc = Document(html, url=url)
    return HtmlArticle(doc.short_title(), doc.summary(), url)


def make_header(article):
    return E.header(E.h1(article.title), E.a(article.url, href=article.url))


def insert_header(article):
    html = ET.HTML(article.content)
    html.find("body").insert(0, make_header(article))

    return tostring(html, encoding="unicode", pretty_print=True)


def main(url):
    res = requests.get(url)
    retrieved_at = datetime.now()

    article = extract_article(res.text, url)
    html = insert_header(article)

    save(html, filepath(article.title, retrieved_at))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("url", type=str, help="url to get")
    args = parser.parse_args()

    main(args.url)
