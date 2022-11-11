from entities.Point import Point


class DetectInfo(object):
    "yoloで取得した情報(ラベル、座標)を格納する"

    def __init__(self, label: int, x: int, y: int, w: int, h: int):
        self._label = label
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    @property
    def label(self) -> int:
        return self._label

    @property
    def rect(selft) -> tuple:
        "座標を返す x,y,w,h"
        return (selft._x, selft._y, selft._w, selft._h)

    def convert2CenterPoint(self) -> Point:
        """
        中心座標にして返す
        """

        center_x: int = (self._x + self._w) / 2
        center_y: int = (self._y + self._h) / 2
        return Point(int(center_x), int(center_y))

    def loadLabels(label_path: str) -> list:
        """
        ラベルを読み込む
        @input
            label_path  : yoloの出力結果の保存パス
        @return 
            DetectInfo  : 出力結果
        """

        detect_list: list[DetectInfo] = []

        try:
            with open(label_path, "r") as f:
                lines: list[str] = f.readlines()
                if len(lines) == 0:
                    return []

                for line in lines:
                    yolo_data = line.split(" ")
                    print(yolo_data)

                    if len(yolo_data) == 0:
                        continue

                    label = int(float(yolo_data[0]))

                    x = int(float(yolo_data[1]))
                    y = int(float(yolo_data[2]))
                    w = int(float(yolo_data[3]))
                    h = int(float(yolo_data[4]))

                    detect_list.append(DetectInfo(label, x, y, w, h))

                return detect_list

        except Exception as e:
            raise e
