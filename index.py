from datetime import datetime
from pathlib import Path

from lxml import etree as ET

import settings

NO_TITLE = "Untitled"
TITLE_DIVIDER = "|"


class Article:
    @property
    def title(self):
        return self._title

    def __init__(self, path, title, saved_at):
        self._path = path
        self._title = title
        self._saved_at = saved_at


class ArticleFactory:
    @classmethod
    def from_html_file(cls, path):
        with open(path) as file:
            html = ET.HTML(file.read())
        title = cls._get_title_from_html(html)
        saved_at = cls._get_timestamp_from_filename(path)
        return Article(path, title, saved_at)

    @staticmethod
    def _get_title_from_html(html):
        title = html.find("head/title")
        if title is not None:
            return title.text.partition(TITLE_DIVIDER)[0].strip()
        else:
            return NO_TITLE

    @staticmethod
    def _get_timestamp_from_filename(path):
        return datetime.strptime(path.stem.partition("_")[0], settings.TIMESTAMP_FORMAT)


def main():
    p = Path(settings.ROOT_DIRECTORY) / "unread"

    files = p.glob("*.html")
    articles = [ArticleFactory.from_html_file(f) for f in files]
    for article in articles:
        print(article.title, article._saved_at, article._path)


if __name__ == "__main__":
    main()
