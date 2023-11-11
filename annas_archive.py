import re
from contextlib import closing
from http.client import RemoteDisconnected
from typing import Generator
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import urlopen, Request

from lxml import html
from lxml.etree import Comment

from calibre import browser
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog
from calibre_plugins.store_annas_archive.constants import DEFAULT_MIRRORS, SearchOption

try:
    from qt.core import QUrl
except (ImportError, ModuleNotFoundError):
    from PyQt5.Qt import QUrl

SearchResults = Generator[SearchResult, None, None]

INFO_PATTERN = re.compile(r'(?:(.+) \[(.*)\], )?([a-z0-9]{3,7})(?:, ([\d.]+(?:KB|MB|GB)))?(?:, (.+))?')


class AnnasArchiveStore(StorePlugin):
    def genesis(self):
        self.working_mirror = None

    def _search(self, url: str, max_results: int, timeout: int) -> SearchResults:
        br = browser()
        doc = None
        for self.working_mirror in self.config.get('mirrors', DEFAULT_MIRRORS):
            with closing(br.open(url.format(base=self.working_mirror), timeout=timeout)) as resp:
                if resp.code < 500 or resp.code > 599:
                    doc = html.fromstring(resp.read())
                    break
        if doc is None:
            self.working_mirror = None
            raise Exception('No working mirrors of Anna\'s Archive found.')
        counter = max_results
        for data in doc.xpath('//div[@class="mb-4"]/div[contains(@class,"h-[125]")]'):
            if counter <= 0:
                break

            book = data
            if not book.xpath('./*'):
                comments = tuple(book.iterchildren(Comment))
                if comments:
                    book = html.fromstring(html.tostring(comments[0]).strip(b'<!--').strip(b'-->'))
                else:
                    continue

            hash_id = ''.join(url.split('/')[-1] for url in book.xpath('./a/@href'))
            if not hash_id:
                continue

            s = SearchResult()
            s.detail_item = hash_id
            s.cover_url = ''.join(book.xpath('./a/div[contains(@class,"flex-none")]/div/img/@src'))
            s.title = ''.join(book.xpath('./a/div/h3/text()'))
            s.author = ''.join(book.xpath('./a/div/div[contains(@class,"italic")]/text()'))

            info = ''.join(book.xpath('./a/div/div[contains(@class,"text-gray-500")]/text()'))
            match = INFO_PATTERN.match(info)
            if match is not None:
                s.formats = match.group(3).upper()

            s.price = '$0.00'
            s.drm = SearchResult.DRM_UNLOCKED

            counter -= 1
            yield s

    def search(self, query, max_results=10, timeout=60) -> SearchResults:
        url = f'{{base}}/search?q={quote_plus(query)}'
        search_opts = self.config.get('search', {})
        for option in SearchOption.options:
            value = search_opts.get(option.config_option, ())
            if isinstance(value, str):
                value = (value,)
            for item in value:
                url += f'&{option.url_param}={item}'
        yield from self._search(url, max_results, timeout)

    def open(self, parent=None, detail_item=None, external=False):
        if detail_item:
            url = self._get_url(detail_item)
        else:
            url = self.working_mirror
        if external or self.config.get('open_external', False):
            open_url(QUrl(url))
        else:
            d = WebStoreDialog(self.gui, self.working_mirror, parent, url)
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get('tags', ''))
            d.exec()

    def get_details(self, search_result: SearchResult, timeout=60):
        if not search_result.formats:
            return

        _format = '.' + search_result.formats.lower()

        link_opts = self.config.get('link', {})
        url_extension = link_opts.get('url_extension', True)
        content_type = link_opts.get('content_type', False)
        sub_site = link_opts.get('sub_site', False)

        br = browser()
        with closing(br.open(self._get_url(search_result.detail_item), timeout=timeout)) as f:
            doc = html.fromstring(f.read())
        for link in doc.xpath('//div[@id="md5-panel-downloads"]/div/ul/li/a[contains(@class, "js-download-link")]'):
            url = link.get('href')
            if url[0] == '/':
                url = self.working_mirror + url
            link_text = ''.join(link.itertext())
            if link_text == 'Bulk torrent downloads':  # Ignore the link to datasets
                continue

            is_sub_site = False
            if sub_site:
                is_sub_site = True
                if link_text == 'Libgen.li':
                    url = self._get_libgen_link(url, br, True)
                elif link_text == 'Libgen.rs Fiction' and link_text == 'Libgen.rs Non-Fiction':
                    url = self._get_libgen_link(url, br, False)
                elif link_text.startswith('Sci-Hub'):
                    url = self._get_scihub_link(url, br)
                else:
                    is_sub_site = False

            if not is_sub_site:
                # Speeds it up by checking the extension of the url.
                # Might miss a direct url that doesn't end with the extension
                if url_extension and not url.endswith(_format):
                    continue
                # Takes longer, but more accurate
                if content_type:
                    try:
                        with urlopen(Request(url, method='HEAD'), timeout=timeout) as resp:
                            if resp.info().get_content_maintype() != 'application':
                                continue
                    except (HTTPError, URLError, TimeoutError, RemoteDisconnected):
                        pass

            search_result.downloads[f"{link_text}.{search_result.formats}"] = url

    @staticmethod
    def _get_libgen_link(url: str, br, add_prefix: bool) -> str:
        with closing(br.open(url)) as resp:
            doc = html.fromstring(resp.read())
            scheme, _, host, _ = resp.geturl().split('/', 3)
        url = ''.join(doc.xpath('//a[h2[text()="GET"]]/@href'))
        if add_prefix:
            return f"{scheme}//{host}/{url}"
        else:
            return url

    @staticmethod
    def _get_scihub_link(url, br):
        with closing(br.open(url)) as resp:
            doc = html.fromstring(resp.read())
            scheme, _ = resp.geturl().split('/', 1)
        url = ''.join(doc.xpath('//embed[@id="pdf"]/@src'))
        return scheme + url

    def _get_url(self, md5):
        return f"{self.working_mirror}/md5/{md5}"

    def config_widget(self):
        from calibre_plugins.store_annas_archive.config import ConfigWidget
        return ConfigWidget(self)

    def save_settings(self, config_widget):
        config_widget.save_settings()
