#docker build -t george9971/ap2n:latest . --no-cache
# git cloneキャッシュ対策でdummyファイルを作成する
touch dummyfile && docker build -t george9971/ap2n:latest .
