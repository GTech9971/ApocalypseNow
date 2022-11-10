FROM ultralytics/yolov5:latest
WORKDIR /usr/src/app/
#yolov5のモジュールのパスを通す
ENV PYTHONPATH /usr/src/app
#api-serverのclone& 必須ライブラリのインストール
RUN git clone https://github.com/GTech9971/ApocalypseNow.git
WORKDIR /usr/src/app/ApocalypseNow/api-server/
# api-db用のライブラリをインストール
RUN apt-get update && apt-get -y install gcc libmariadb-dev    
RUN pip install -r requirements.txt
#api-server立ち上げ
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]