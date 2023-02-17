import logging
import requests
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup as bs
from utils import verbose_get, write_file, cleanse_filename


requests.get = verbose_get(requests.get)


class PDFripper():
    def __init__(self, url, dry_run: bool = False):
        self.logger = logging.getLogger(__name__)
        self.dry_run = dry_run
        self.url = url
        self.base_url = url
        self.page = url

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        self._page = requests.get(value)
        self._page.raise_for_status()

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        url = urlsplit(value)
        self._base_url = urlunsplit((url.scheme, url.netloc, '', '', ''))

    @staticmethod
    def pdf_filter(tag):
        return (tag.get('data-pdf', '') == 'true') \
            | ('pdf' in tag.get('type', ''))

    @staticmethod
    def label(tag):
        return tag.get('title', False) \
            or tag.get('href', False).rsplit('/', 1)[-1]

    def pdfs(self) -> list:
        soup = bs(self.page.text, 'html.parser')
        return soup.find_all(self.pdf_filter)

    def extract(self, path, pdfs: list = None):
        pdfs = pdfs if pdfs is not None else self.pdfs()
        pdfs = ((self.label(pdf),
                 requests.get(self.base_url+pdf.get('href'),
                              dry_run=self.dry_run)) for pdf in pdfs)
        for label, pdf in pdfs:
            filename = cleanse_filename(label)
            content = pdf.content if self.dry_run is False else None
            write_file(path, filename, content, dry_run=self.dry_run)
