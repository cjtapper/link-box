from pathlib import Path

from lxml import etree as ET

import settings

NO_TITLE = "Untitled"
TITLE_DIVIDER = "|"


class Article:
    @property
    def title(self):
        return self._title

    def __init__(self, path, title):
        self._path = path
        self._title = title


class ArticleFactory:
    @classmethod
    def from_html_file(cls, path):
        with open(path) as file:
            html = ET.HTML(file.read())
        title = cls._get_title_from_html(html)
        return Article(path, title)

    @staticmethod
    def _get_title_from_html(html):
        title = html.find("head/title")
        if title is not None:
            return title.text.partition(TITLE_DIVIDER)[0].strip()
        else:
            return NO_TITLE


def main():
    p = Path(settings.ROOT_DIRECTORY) / "unread"

    files = p.glob("*.html")
    articles = [ArticleFactory.from_html_file(f) for f in files]
    for article in articles:
        print(article.title)


if __name__ == "__main__":
    main()
