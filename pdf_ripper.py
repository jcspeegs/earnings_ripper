import requests
import os
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup as bs


class PDFripper():
    def __init__(self, url):
        self.url = url
        self.base_url = url
        self.page = url

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        self._page = requests.get(value)

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        url = urlsplit(value)
        self._base_url = urlunsplit((url.scheme, url.netloc, '', '', ''))

    def pdfs(self) -> list:
        soup = bs(self.page.text, 'html.parser')
        return [link.get('href') for link in soup.find_all('a')
                if link.get('data-pdf') == 'true']

    def extract(self, path, pdfs: list = None):
        pdfs = pdfs if pdfs is not None else self.pdfs()
        pdfs = [requests.get(self.base_url+pdf) for pdf in pdfs]
        for pdf in pdfs:
            file = pdf.url.rsplit('/', 1)[-1]
            file = os.path.join(path, file)
            with open(file, 'wb') as fl:
                fl.write(pdf.content)
