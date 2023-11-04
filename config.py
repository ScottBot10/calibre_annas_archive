from collections import OrderedDict

from qt.core import QWidget, QGridLayout, QLabel, QComboBox, QSpacerItem, QFrame, QCheckBox, QSizePolicy

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
        self.resize(250, 240)

        self.grid = QGridLayout(self)

        self.grid.addWidget(QLabel(_('Default Ordering:'), self), 0, 0)
        self.order = QComboBox(self)
        for txt, order in _ORDERS.items():
            self.order.addItem(txt, order)
        self.order.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.grid.addWidget(self.order, 0, 1)

        self.grid.addWidget(QLabel(_('Download link options:'), self), 1, 0, 1, 2)
        frame = QFrame(self)
        link_options = QGridLayout(frame)
        link_options.setContentsMargins(0, 0, 0, 0)
        link_options.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 0)
        self.url_extension = QCheckBox(_('Verify url extension'), frame)
        link_options.addWidget(self.url_extension, 0, 1)
        self.content_type = QCheckBox(_('Verify Content-Type'), frame)
        link_options.addWidget(self.content_type, 1, 1)
        self.sub_site = QCheckBox(_('Get from sub site'), frame)
        link_options.addWidget(self.sub_site, 2, 1)

        self.grid.addWidget(frame, 2, 0, 1, 2)

        self.open_external = QCheckBox(_('Open store in external web browser'), self)
        self.grid.addWidget(self.open_external, 3, 0, 1, 2)

        self.load_settings()

    def load_settings(self):
        config = self.store.config

        self.open_external.setChecked(config.get('open_external', False))
        self.order.setCurrentIndex(list(_ORDERS.values()).index(config.get('order', 0)))

        link_opts = config.get('link', {})
        self.url_extension.setChecked(link_opts.get('url_extension', True))
        self.content_type.setChecked(link_opts.get('content_type', False))
        self.sub_site.setChecked(link_opts.get('sub_site', False))

    def save_settings(self):
        self.store.config['open_external'] = self.open_external.isChecked()
        self.store.config['order'] = self.order.currentData()
        self.store.config['link'] = {
            'url_extension': self.url_extension.isChecked(),
            'content_type': self.content_type.isChecked(),
            'sub_site': self.sub_site.isChecked()
        }
