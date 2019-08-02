import os
import re
from datetime import datetime
from pathlib import Path

import requests
from readability import Document

TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S"

directory = os.getenv("READIT")

res = requests.get(
    "https://arstechnica.com/tech-policy/2019/08/navy-pilot-dead-after-crash-in-star-wars-canyon-in-death-valley/"
)
timestamp = datetime.now()

doc = Document(res.text)


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


def filepath(doc):
    filename = get_valid_filename(
        timestamp.strftime(TIMESTAMP_FORMAT) + " " + doc.title()
    )

    p = Path(directory) / "unread" / (filename + ".html")
    return p


os.makedirs(Path(directory) / "unread", exist_ok=True)
with open(filepath(doc), "w") as f:
    f.write(doc.summary())
