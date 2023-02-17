import logging
import functools
import requests
import os
from urllib.parse import urlsplit, urlunsplit
import re
from bs4 import BeautifulSoup as bs


def verbose_get(func):
    @functools.wraps(func)
    def wrapper(url, dry_run=False, *args, **kwargs):
        logging.info(f'Ripping {url}')
        if dry_run is True:
            return url
        else:
            return func(url, *args, **kwargs)
    return wrapper


requests.get = verbose_get(requests.get)


def cleanse_filename(filename: str):
    replace = ' ()-_'
    pattern = f"[{''.join([re.escape(char) for char in replace])}]+"
    return re.sub(pattern, '_', filename).strip('_').lower()


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
            file = os.path.join(path, cleanse_filename(label))
            self.logger.info(f'writing {file}')
            if self.dry_run is not True:
                with open(file, 'wb') as fl:
                    fl.write(pdf.content)
