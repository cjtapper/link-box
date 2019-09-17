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

from . import settings

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
    filename = get_valid_filename(
        timestamp.strftime(settings.TIMESTAMP_FORMAT) + " " + title
    )
    p = Path(settings.ROOT_DIRECTORY) / "unread" / (filename + ".html")
    return p


def save(html, filepath):
    os.makedirs(Path(settings.ROOT_DIRECTORY) / "unread", exist_ok=True)
    with open(filepath, "w") as f:
        f.write(html)


def extract_article(html, url):
    doc = Document(html, url=url)
    return HtmlArticle(doc.short_title(), doc.summary(html_partial=True), url)


def make_header(article):
    return E.header(E.h1(article.title), E.a(article.url, href=article.url))


def page_title(title):
    return f"{title} | {settings.NAME}"


def generate_article_html(article):
    html = E.html(
        E.head(E.title(page_title(article.title))),
        E.body(make_header(article), ET.HTML(article.content)),
    )

    return tostring(html, encoding="unicode", pretty_print=True)


def main(url):
    res = requests.get(url)
    retrieved_at = datetime.now()

    article = extract_article(res.text, url)
    html = generate_article_html(article)

    save(html, filepath(article.title, retrieved_at))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("url", type=str, help="url to get")
    args = parser.parse_args()

    main(args.url)
