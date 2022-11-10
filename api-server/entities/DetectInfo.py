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

    # TODO ロジックの実装
    def convert2CenterPoint(self) -> Point:
        """
        中心座標にして返す
        """
        pass

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
                    yolo_data = line[0].split(" ")
                    label = int(yolo_data[0])

                    x = int(yolo_data[1])
                    y = int(yolo_data[2])
                    w = int(yolo_data[3])
                    h = int(yolo_data[4])

                    detect_list.append(DetectInfo(label, x, y, w, h))

                return detect_list

        except Exception as e:
            raise e
