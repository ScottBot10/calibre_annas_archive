from collections import OrderedDict
from typing import Dict

from calibre_plugins.store_annas_archive.search_options import SearchConfiguration, Content, Access, FileType, Source, \
    Language
from qt.core import Qt, QWidget, QGridLayout, QVBoxLayout, QLabel, QFrame, QGroupBox, QScrollArea, QAbstractScrollArea, \
    QComboBox, QSpacerItem, QCheckBox, QSizePolicy

load_translations()

_ORDERS = OrderedDict({
    _('Most relevant'): '',
    _('Newest'): 'newest',
    _('Oldest'): 'oldest',
    _('Largest'): 'largest',
    _('Smallest'): 'smallest'
})


class ConfigWidget(QWidget):
    def __init__(self, store):
        super().__init__()
        self.store = store
        self.resize(575, 640)

        main_layout = QVBoxLayout(self)

        search_options = QGroupBox(_('Search options'), self)
        search_options.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        search_grid = QGridLayout(search_options)
        search_grid.setContentsMargins(3, 3, 3, 9)

        search_grid.addWidget(QLabel(_('Ordering:'), search_options), 0, 0)
        self.order = QComboBox(search_options)
        for txt, order in _ORDERS.items():
            self.order.addItem(txt, order)
        self.order.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        search_grid.addWidget(self.order, 0, 1, 1, 2)

        self.search_options: Dict[str, SearchConfiguration] = {}

        search_grid.addWidget(self._make_cbx_group(search_options, Content()), 1, 0)
        search_grid.addWidget(self._make_cbx_group(search_options, Access()), 2, 0)
        search_grid.addWidget(self._make_cbx_group(search_options, FileType()), 1, 1)
        search_grid.addWidget(self._make_cbx_group(search_options, Source()), 2, 1)
        search_grid.addWidget(self._make_cbx_group(search_options, Language(), scrollbar=True), 1, 2, 2, 1)

        main_layout.addWidget(search_options)

        link_options = QGroupBox(_('Download link options'), self)
        link_options.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        link_layout = QGridLayout(link_options)
        link_layout.setContentsMargins(0, 0, 0, 3)
        link_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 0)
        self.url_extension = QCheckBox(_('Verify url extension'), link_options)
        link_layout.addWidget(self.url_extension, 0, 1)
        self.content_type = QCheckBox(_('Verify Content-Type'), link_options)
        link_layout.addWidget(self.content_type, 1, 1)
        self.sub_site = QCheckBox(_('Get from sub site'), link_options)
        link_layout.addWidget(self.sub_site, 2, 1)
        main_layout.addWidget(link_options)

        self.open_external = QCheckBox(_('Open store in external web browser'), self)
        self.open_external.clicked.connect(lambda: print(self.geometry(), self.frameGeometry()))
        main_layout.addWidget(self.open_external)

        self.load_settings()

    def _make_cbx_group(self, parent, option: SearchConfiguration, scrollbar: bool = False):
        box = QGroupBox(_(option.name), parent)
        vertical_layout = QVBoxLayout(box)
        if scrollbar:
            vertical_layout.setSpacing(0)
            vertical_layout.setContentsMargins(0, 0, 0, 0)

            scroll_area = QScrollArea(box)
            scroll_area.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
            scroll_area.setFrameShape(QFrame.Shape.NoFrame)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

            cbx_parent = QWidget()
            cbx_parent.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
            top_vertical = vertical_layout
            vertical_layout = QVBoxLayout(cbx_parent)
        else:
            cbx_parent = box

        vertical_layout.setSpacing(3)
        vertical_layout.setContentsMargins(3, 3, 3, 3)

        for name, type_ in option.options:
            check_box = QCheckBox(cbx_parent)
            check_box.setText(name)
            vertical_layout.addWidget(check_box)
            option.checkboxes[type_] = check_box
        self.search_options[option.config_option] = option
        if scrollbar:
            scroll_area.setWidget(cbx_parent)
            top_vertical.addWidget(scroll_area)
        return box

    def load_settings(self):
        config = self.store.config

        self.open_external.setChecked(config.get('open_external', False))

        search_opts = config.get('search', {})
        self.order.setCurrentIndex(list(_ORDERS.values()).index(search_opts.get('order', '')))
        for configuration in self.search_options.values():
            for type_ in search_opts.get(configuration.config_option, []):
                if type_ in configuration.checkboxes:
                    configuration.checkboxes[type_].setChecked(True)

        link_opts = config.get('link', {})
        self.url_extension.setChecked(link_opts.get('url_extension', True))
        self.content_type.setChecked(link_opts.get('content_type', False))
        self.sub_site.setChecked(link_opts.get('sub_site', False))

    def save_settings(self):
        self.store.config['open_external'] = self.open_external.isChecked()

        self.store.config['search'] = dict(
            order=self.order.currentData(),
            **{
                configuration.config_option: [type_
                                              for type_, cbx in configuration.checkboxes.items() if cbx.isChecked()]
                for configuration in self.search_options.values()
            }
        )
        self.store.config['link'] = {
            'url_extension': self.url_extension.isChecked(),
            'content_type': self.content_type.isChecked(),
            'sub_site': self.sub_site.isChecked()
        }
