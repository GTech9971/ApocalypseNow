# ApocalypseNow

ハイテク御座敷シューター支援ソフト
 
## yolov5 環境構築

以下のコマンドを実行してdocker-compose.ymlをup

```
docker compose -f "yolo_works/docker-compose.yaml" up -d --build 
```


以下のコマンドでコンテナ内に入る
```
docker exec -it yolo_works-yolov5lst-1 /bin/bash
```

[参考ページ](https://kikaben.com/yolov5-docker-deployment/)

## yolov5 学習

コンテナ内で以下のコマンドを実行して学習を開始する

```
python train.py --img 640 --batch 16 --epochs 200 --data {sample.yamlのpath} --weights yolov5s.pt
```

## tensorboard
コンテナ内に入り以下のコマンドでtensorboardを起動できる
```
tensorboard --logdir runs/train
```

閲覧はホストマシンでlocalhost:6006に入れば表示される。

学習とtensorboardの起動を一緒に行いたい場合は、以下のコマンドを実行する
```
python train.py --img 640 --batch 16 --epochs 200 --data {sample.yamlのpath} --weights yolov5s.pt | tensorboard --logdir runs/train
```