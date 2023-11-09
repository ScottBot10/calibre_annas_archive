# [Anna's Archive Calibre Store](https://github.com/ScottBot10/calibre_annas_archive)

A [Calibre](https://calibre-ebook.com/) store plugin for [Anna's Archive](https://annas-archive.org/).
> 📚 The world’s largest open-source open-data library. ⭐️ Mirrors Sci-Hub, Library Genesis, Z-Library, and more.

## Usage
To add this plugin, download the latest .zip release, 
then in Calibre go to **Preferences > Plugins**, click **Load plugin from file** and select your downloaded zip file.

You could also install it from the source by cloning this repository and running
```shell
calibre-customize -b <path to cloned repo>
```
or if you're on Linux, you can run the shell script to create the zip file and then add that
```shell
./zip_release.sh && calibre-customize -a $(ls calibre_annas_archive-v*.zip -1rt | tail -n1)
```