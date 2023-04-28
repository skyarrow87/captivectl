# CaptiveCTL
## キャプティブポータルの自動ログインツール

### Uses / 使用方法
```
captivectl.py /path/to/config.txt
```

### Build / ビルド
pipenvで環境を構築
```
pipenv install
```


Linuxの場合 ```patchelf```と```ccache```が必要

nuitkaでビルド
```
nuitka3 --standalone --onefile captivectl.py 
```