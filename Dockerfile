FROM ultralytics/yolov5:latest
WORKDIR /usr/src/app/
#yolov5のモジュールのパスを通す
RUN export PYTHONPATH="/usr/src/app:$PYTHONPATH"
#api-serverのclone& 必須ライブラリのインストール
RUN git clone https://github.com/GTech9971/ApocalypseNow.git
WORKDIR /usr/src/app/ApocalypseNow/api-server/
RUN pip install -r requirements.txt
#api-server立ち上げ
RUN python main.py