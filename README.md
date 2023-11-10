# [Anna's Archive Calibre Store](https://github.com/ScottBot10/calibre_annas_archive)

A [Calibre](https://calibre-ebook.com/) store plugin for [Anna's Archive](https://annas-archive.org/).
> 📚 The world’s largest open-source open-data library. ⭐️ Mirrors Sci-Hub, Library Genesis, Z-Library, and more.

## Usage
To add this plugin, go to the latest [release](https://github.com/ScottBot10/calibre_annas_archive/releases)
and download the file that looks like `calibre_annas_archive-vx.x.x.zip` where the x's are the version number, 
then in Calibre go to `Preferences > Plugins`, click `Load plugin from file` and select your downloaded zip file.

You could also install it from the source by cloning this repository and running:
```shell
calibre-customize -b <path to cloned repo>
```
or if you're on Linux, you can run the shell script to create the zip file and then add that:
```shell
./zip_release.sh && calibre-customize -a $(ls calibre_annas_archive-v*.zip -1rt | tail -n1)
```

## Configuration
You can change configuration by going to 
`Preferences > Plugins > Store` and scrolling down to and double-clicking `Anna's Archive (x.x.x) by ScottBot10`
to open the settings menu.

### Search Options
This plugin has the same search options as the actual site.
For each checkbox option e.g. filetype, language: if no boxes are checked, then it doesn't filter on that option.
But if any are checked then it will only show results that match that selection.

### Download link options
These options affect what files are shown in the downloads of the search (the green button),
they don't affect opening the book in the browser.
- **Get from sub site:** Whether to get direct download links from external sites such and Libgen or SciHub
- **Verify Content-Type:** Make a HEAD request to each site and check if it has an 'application' Content-Type
- **Verify url extension:** Check whether the url ends with the extension of the file's format

### Mirrors
This is a list of mirrors that the plugin will try, in the specified order, to access.
You can change the order of, delete, and add mirror urls.