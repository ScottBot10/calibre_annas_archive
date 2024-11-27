from collections import OrderedDict
from typing import Iterable, Dict, List, Type, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from qt.core import QCheckBox, QComboBox

__all__ = (
    'DEFAULT_MIRRORS', 'SearchOption', 'SearchConfiguration', 'CheckboxConfiguration', 'Order', 'Content', 'Access',
    'FileType', 'Source', 'Language'
)

DEFAULT_MIRRORS = ['https://annas-archive.org', 'https://annas-archive.li', 'https://annas-archive.se']
RESULTS_PER_PAGE = 100


class SearchOption(type):
    """
    Factory class for SearchConfigurations
    """

    options: List[Type['SearchConfiguration']] = []

    def __new__(mcs, name: str, config_option: str, url_param: str, base: 'SearchConfiguration',
                options: Iterable[Tuple[str, str]]):
        values = tuple(option[1] for option in options)
        cls = super().__new__(mcs, name, (base,), {'name': name, 'config_option': config_option, 'url_param': url_param,
                                                   'options': options, 'values': values})
        mcs.options.append(cls)
        return cls

    def __init__(cls, name: str, config_option: str, url_param: str, base: 'SearchConfiguration',
                 options: Iterable[Tuple[str, str]]):
        super().__init__(cls)


class SearchConfiguration:
    name: str
    config_option: str
    url_param: str
    options: Iterable[Tuple[str, str]]
    values: Tuple[str]
    default = ''

    def __init__(self, combo_box):
        self.combo_box: 'QComboBox' = combo_box

    def to_save(self):
        return self.combo_box.currentData()

    def load(self, value):
        self.combo_box.setCurrentIndex(self.values.index(value))


class CheckboxConfiguration(SearchConfiguration):
    default = []

    def __init__(self):
        self.checkboxes: Dict[str, 'QCheckBox'] = {}

    def to_save(self):
        return [type_ for type_, cbx in self.checkboxes.items() if cbx.isChecked()]

    def load(self, value):
        for type_ in value:
            if type_ in self.checkboxes:
                self.checkboxes[type_].setChecked(True)


Order = SearchOption('Order', 'order', 'sort', SearchConfiguration, (
    ('Most relevant', ''),
    ('Newest (publication year)', 'newest'),
    ('Oldest (publication year)', 'oldest'),
    ('Largest', 'largest'),
    ('Smallest', 'smallest'),
    ('Newest (open sourced)', 'newest_added'),
    ('Oldest (open sourced)', 'oldest_added')
))
Content = SearchOption('Content', 'content', 'content', CheckboxConfiguration, (
    ('Book (non-fiction)', 'book_nonfiction'),
    ('Book (fiction)', 'book_fiction'),
    ('Book (unknown)', 'book_unknown'),
    ('Magazine', 'magazine'),
    ('Comic book', 'book_comic'),
    ('Standards Document', 'standards_document'),
    ('Other', 'other'),
    ('Musical score', 'musical_score'),
    ('Audiobook', 'audiobook'),
))
Access = SearchOption('Access', 'access', 'acc', CheckboxConfiguration, (
    ('Partner Server download', 'aa_download'),
    ('External download', 'external_download'),
    ('External borrow', 'external_borrow'),
    ('External borrow (print disabled)', 'external_borrow_printdisabled'),
    ('Contained in torrents', 'torrents_available')
))
FileType = SearchOption('Filetype', 'filetype', 'ext', CheckboxConfiguration, tuple(zip(
    *((('epub', 'mobi', 'pdf', 'azw3', 'cbr', 'cbz', 'fb2', 'djvu', 'txt'),) * 2)
)))
Source = SearchOption('Source', 'source', 'src', CheckboxConfiguration, (
    ('Libgen.li', 'lgli'),
    ('Libgen.rs', 'lgrs'),
    ('Sci-Hub', 'scihub'),
    ('Z-Library', 'zlib'),
    ('Internet Archive', 'ia'),
    ('Uploads to AA', 'upload'),
    ('Nexus/STC', 'nexusstc'),
    ('DuXiu', 'duxiu'),
    ('Z-Library Chinese', 'zlibzh'),
    ('MagzDB', 'magzdb'),
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
Language = SearchOption('Language', 'language', 'lang', CheckboxConfiguration, tuple(
    (f"{name} [{code}]" if code != '_empty' else name, code) for name, code in _languages.items()
))
