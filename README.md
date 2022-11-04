# ApocalypseNow

ハイテク御座敷シューター支援ソフト
ターゲットサイトの位置情報をyoloで取得し、着弾位置を表示させる
 
## yolov5 環境構築

[https://github.com/ultralytics/yolov5/wiki/Docker-Quickstart](https://github.com/ultralytics/yolov5/wiki/Docker-Quickstart)

## Dockerでyolov5(GPU)
### 1.Nvidia Driverのインストール
以下のURLにアクセスしてPCに搭載しているGPUのドライバーをインストールする
[https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx)

*Linuxの場合、ダウンロードしてきたドライバ名.runをインストールする
以下のコマンドを実行する。

```
chmod +x ドライバ名.run
sudo ./ドライバ名.run
```

*WSLを使用してもドライバーは、Windows用をインストールすればよい。
[参考ページ](https://blog.shikoan.com/wsl2-ndivid-docker-pytorch/#:~:text=%E3%81%AE%E3%82%AA%E3%83%9A%E3%83%AC%E3%83%BC%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E3%81%AF%E3%80%81-,WSL%E3%82%92%E4%BD%BF%E3%81%86%E5%A0%B4%E5%90%88%E3%81%A7%E3%82%82Windows,-%E3%81%AB%E3%81%97%E3%81%BE%E3%81%97%E3%82%87%E3%81%86)

### 2.Docker Engineのインストール
以下のURLを参考にする
[https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

以下公式から

- 古いバージョンのアンインストール
```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

- リポジトリをセットアップする

```
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

- Docker の公式 GPG キーを追加します。

```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

- 次のコマンドを使用して、リポジトリをセットアップします。
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

- aptパッケージ インデックスを更新します。
```
sudo apt-get update
```

- 最新バージョンをインストールするには、次を実行します。

```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

- hello-worldイメージを実行して、Docker エンジンのインストールが成功したことを確認します。

```
sudo docker run hello-world
```


### 3. Nvidia-Dockerのインストール
以下のURLにアクセスしてNvidia-Dockerをホストにインストールする
[https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)

以下公式ページから

- パッケージ リポジトリと GPG キーをセットアップします。

```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

- nvidia-docker2パッケージの一覧を更新した後、パッケージ (および依存関係)をインストールします。

```
sudo apt-get update
```

```
sudo apt-get install -y nvidia-docker2
```

- デフォルトのランタイムを設定した後、Docker デーモンを再起動してインストールを完了します。

```
sudo systemctl restart docker
```

- この時点で、基本の CUDA コンテナーを実行して、動作するセットアップをテストできます。

```
sudo docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```

### 4. yolov5 コンテナ起動

[参考ページ https://kikaben.com/yolov5-docker-deployment/](https://kikaben.com/yolov5-docker-deployment/)

- 以下のコマンドを実行してdocker-compose.ymlをupする

*wslを使用している場合、docker-compose.ymlと学習データをwslにコピーして、wsl上で以下のコマンドを実行する必要がある。自作学習データは/dataにコピーする。

```
docker compose -f "docker-compose.yaml" up -d --build 
```


- 以下のコマンドでコンテナ内に入る

```
docker exec -it yolo_works-yolov5lst-1 /bin/bash
```

- コンテナがGPUを認識しているかを以下のコマンドで確認する

```
nvidia-smi
```


## yolov5 学習

- コンテナ内で以下のコマンドを実行して学習を開始する

```
python train.py --img 640 --batch 16 --epochs 200 --data {sample.yamlのpath} --weights yolov5s.pt
```

### tensorboard
- コンテナ内に入り以下のコマンドでtensorboardを起動できる

```
tensorboard --logdir runs/train
```

- 閲覧はホストマシンで[localhost:6006](localhost:6006)に入れば表示される。

- 学習とtensorboardの起動を一緒に行いたい場合は、以下のコマンドを実行する(バグで学習結果の保存が終わらない時があるので注意)

```
python train.py --img 640 --batch 16 --epochs 200 --data {sample.yamlのpath} --weights yolov5s.pt | tensorboard --logdir runs/train
```

### 学習結果
- コンテナ以下のフォルダに学習結果が出力される

```
/usr/src/app/runs/train/exp/weights
```

## yolov5 識別
### 画像の識別
先ほどの学習でptファイルが保存されたので、それを使用して以下のコマンドを実行する

```
python detect.py --weights 学習結果.pt --source 画像のパス
```

学習結果は、コンテナ内の以下に保存される

```
/usr/src/app/runs/detect/exp
```

また、上記パスをバインドしているためホストの以下のパスにも反映される

```
./detect_result/
```

## ApocalypseNow API-Server構築
/api-server/Dockerfileをビルドしてイメージを生成する。

```
docker build -t george9971/apocalypse_now . --no-cache
```

/api-server/docker-compose.yamlをupするとapi-serverが立ち上がる。
[http://localhost:8000/docs](http://localhost:8000/docs)へのアクセスでAPIのドキュメントが閲覧できる。


```
docker compose -f "docker-compose.yaml" up -d --build 
```