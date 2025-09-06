# gnome-slideshow-wallpaper-xml-generator
GNOMEデスクトップの壁紙をスライドショー表示させるのに必要なXMLファイルを生成するスクリプトです。

## 注意

このスクリプトは**Slideshow XML Fileの生成のみ**行います。  
作成したスライドショーを壁紙として設定するにはBackground Properties XML Fileを作成してください。  
Background Properties XML Fileの作成方法は[Ubuntu documentation | Community Help Wiki > SlideshowWallpapers](https://help.ubuntu.com/community/SlideshowWallpapers)を参照してください。

## 使い方

```shell
uv run main.py -t /path/to/images_directory -o /path/to/output_file.xml
```

## ヘルプ

```shell
uv run main.py --help
```

## 関連ドキュメント

- [Ubuntu documentation | Community Help Wiki > SlideshowWallpapers](https://help.ubuntu.com/community/SlideshowWallpapers)
