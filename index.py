from pathlib import Path

from lxml import etree as ET

import settings

NO_TITLE = "Untitled"
TITLE_DIVIDER = "|"


class Article:
    @property
    def title(self):
        return self._title

    def __init__(self, path):
        self._path = path
        with open(self._path) as file:
            html = ET.HTML(file.read())
        self._set_title_from_html(html)

    def _set_title_from_html(self, html):
        title = html.find("head/title")
        if title is not None:
            self._title = title.text.partition(TITLE_DIVIDER)[0].strip()
        else:
            self._title = NO_TITLE


def main():
    p = Path(settings.ROOT_DIRECTORY) / "unread"

    files = p.glob("*.html")
    articles = [Article(f) for f in files]
    for article in articles:
        print(article.title)


if __name__ == "__main__":
    main()
