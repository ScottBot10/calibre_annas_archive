from collections import OrderedDict
from typing import Iterable, Dict, List, Type, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from qt.core import QCheckBox

__all__ = (
    'DEFAULT_MIRRORS', 'SearchOption', 'SearchConfiguration', 'Content', 'Access', 'FileType', 'Source', 'Language')

DEFAULT_MIRRORS = ['https://annas-archive.org', 'https://annas-archive.gs', 'https://annas-archive.se']


class SearchOption(type):
    options: List[Type['SearchConfiguration']] = []

    def __new__(mcs, name: str, config_option: str, url_param: str, options: Iterable[Tuple[str, str]]):
        cls = super().__new__(mcs, name, (SearchConfiguration,),
                              {'name': name, 'config_option': config_option, 'url_param': url_param,
                               'options': options})
        mcs.options.append(cls)
        return cls

    def __init__(cls, *a, **kw):
        super().__init__(cls)


class SearchConfiguration:
    name: str
    config_option: str
    url_param: str
    options: Iterable[Tuple[str, str]]

    def __init__(self):
        self.checkboxes: Dict[str, 'QCheckBox'] = {}


Content = SearchOption('Content', 'content', 'content', (
    ('Book (non-fiction)', 'book_nonfiction'),
    ('Book (fiction)', 'book_fiction'),
    ('Book (unknown)', 'book_unknown'),
    ('Journal article', 'journal_article'),
    ('Comic book', 'book_comic'),
    ('Magazine', 'magazine'),
    ('Standards Document', 'standards_document'),
))
Access = SearchOption('Access', 'access', 'acc', (
    ('Partner Server download', 'aa_download'),
    ('External download', 'external_download'),
    ('External borrow', 'external_borrow'),
    ('External borrow (print disabled)', 'external_borrow_printdisabled')
))
FileType = SearchOption('Filetype', 'filetype', 'ext', tuple(zip(
    *((('epub', 'mobi', 'pdf', 'azw3', 'cbr', 'cbz', 'fb2', 'djvu', 'fb2.zip'),) * 2)
)))
Source = SearchOption('Source', 'source', 'src', (
    ('Libgen.li', 'lgli'),
    ('Libgen.rs', 'lgrs'),
    ('Sci-Hub', 'scihub'),
    ('Z-Library', 'zlib'),
    ('Internet Archive', 'ia'),
))

_languages = OrderedDict({
    'Unknown language': '_empty', 'English': 'en', 'Spanish': 'es', 'Italian': 'it', 'Portuguese': 'pt', 'French': 'fr',
    'German': 'de', 'Chinese': 'zh', 'Turkish': 'tr', 'Dutch': 'nl', 'Hungarian': 'hu', 'Catalan': 'ca',
    'Romanian': 'ro', 'Russian': 'ru', 'Czech': 'cs', 'Lithuanian': 'lt', 'Greek': 'el', 'Polish': 'pl', 'Danish': 'da',
    'Croatian': 'hr', 'Korean': 'ko', 'Hindi': 'hi', 'Japanese': 'ja', 'Latvian': 'lv', 'Latin': 'la',
    'Indonesian': 'id', 'Swedish': 'sv', 'Hebrew': 'he', 'Bangla': 'bn', 'Norwegian': 'no', 'Ukrainian': 'uk',
    'Luxembourgish': 'lb', 'Arabic': 'ar', 'Irish': 'ga', 'Welsh': 'cy', 'Bulgarian': 'bg', 'Tamil': 'ta',
    'Traditional Chinese': 'zh-Hant', 'Afrikaans': 'af', 'Persian': 'fa', 'Serbian': 'sr', 'Belarusian': 'be',
    'Dongxiang': 'sce', 'Vietnamese': 'vi', 'Urdu': 'ur', 'Flemish': 'nl-BE', 'Ndolo': 'ndl', 'Kazakh': 'kk'
})
Language = SearchOption('Language', 'language', 'lang', tuple(
    (f"{name} [{code}]" if code != '_empty' else name, code) for name, code in _languages.items()
))
