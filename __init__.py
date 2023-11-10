from calibre.customize import StoreBase


class AnnasArchiveStore(StoreBase):
    name                = 'Anna\'s Archive'
    description         = 'The world\'s largest open-source open-data library.'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'ScottBot10'
    version             = (0, 2, 0)
    formats             = ['EPUB', 'MOBI', 'PDF', 'AZW3', 'CBR', 'CBZ', 'FB2']
    drm_free_only       = True

    actual_plugin = 'calibre_plugins.store_annas_archive.annas_archive:AnnasArchiveStore'
