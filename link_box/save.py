from collections import namedtuple

from readability import Document

HtmlArticle = namedtuple("HtmlArticle", ["title", "content", "url"])


def extract_article(html, url):
    doc = Document(html, url=url)
    return HtmlArticle(doc.short_title(), doc.summary(html_partial=True), url)
