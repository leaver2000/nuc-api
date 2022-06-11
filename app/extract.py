import re
from itertools import islice
from pathlib import Path
from shutil import copyfileobj
from typing import Iterator, Optional, Callable
from urllib.parse import urljoin

from requests import Session
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

class ApacheNode:
    """
    This represents a tree node in the Apache directory page for the NOAA NOMADS site;
    for more details see https://nomads.ncep.noaa.gov/

    It's used to look up TSRAGR data. TSRAGR is Terminal Aerodrome Forecast (TAF) code
    for a thunderstorm with hail.
    """

    def __init__(self, session: Session, url: str, name: Optional[str] = None) -> None:
        self.session = session
        self.url = url

        if name is None:
            name = url.removesuffix("/").rsplit("/", maxsplit=1)[-1]
        self.name = name

    def __repr__(self) -> str:
        return self.url


class ApacheFile(ApacheNode):
    def download(self, save_to: Path) -> None:
        print(f"Downloading {self.name}...", end=" ")
        local_filename = save_to / self.name

        with self.session.get(self.url, stream=True) as response:
            response.raise_for_status()
            with local_filename.open("wb") as f:
                copyfileobj(response.raw, f)

        print("saved")


class ApacheDir(ApacheNode):
    pre_strainer = SoupStrainer(name="pre")

    # Text has at least one character and cannot contain Parent Directory
    link_pattern = re.compile(
        "(?i)"  # ignore case
        "^"  # string start
        "(?:"  # non-capturing group
        "(?!parent directory)"  # negative lookahead: don't match 'parent directory'
        "."  # match any one character
        ")+"  # match one or more of the above chars
        "$"  # string end
    )

    def __init__(self, session: Session, url: str, name: Optional[str] = None) -> None:
        if not url.endswith("/"):
            url += "/"
        super().__init__(session, url, name)

    def children(self) -> Iterator[ApacheNode]:
        with self.session.get(self.url) as response:
            response.raise_for_status()
            soup = BeautifulSoup(
                markup=response.text, features="lxml", parse_only=self.pre_strainer
            )
        pre = soup.pre
        anchors = pre.find_all(name="a", text=self.link_pattern, recursive=False)

        for anchor in anchors:
            child_name = anchor["href"]
            child_url = urljoin(self.url, child_name)
            size_text = anchor.next_sibling.strip()
            if size_text.endswith("-"):
                child_type = ApacheDir
            else:
                child_type = ApacheFile
            yield child_type(self.session, child_url, child_name)

    def navto(self, *args: str) -> "ApacheDir":
        url = urljoin(self.url, "/".join(args))
        return ApacheDir(self.session, url=url, name=args[-1])

    def inav(self, index: int) -> "ApacheNode":
        (child,) = islice(self.children(), index, index + 1)
        return child

    def iterfiles(self, condition:Callable[[str],bool]=None)-> Iterator["ApacheFile"]:
        for node in self.children():
            if isinstance(node, ApacheFile):
                if not condition:
                    yield node
                elif condition(node.url):
                    yield node


    def iterdir(self) -> Iterator["ApacheDir"]:
        for node in self.children():
            if isinstance(node, ApacheDir):
                yield node