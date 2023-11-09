version=$(grep 'version' __init__.py | sed -r "s/^.*version\s*= \(([0-9]+), ([0-9]+), ([0-9]+)\).*/\1.\2.\3/")

zip "calibre_annas_archive-v${version}.zip" README.md plugin-import-name-store_annas_archive.txt __init__.py annas_archive.py config.py search_options.py