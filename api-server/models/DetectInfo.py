__all__ = ["DetectInfo"]

class DetectInfo(object):
    "yoloで取得した情報(ラベル、座標)を格納する"
    
    def __init__(self, label:int, x:int, y:int, w:int, h:int):
        self._label = label
        self._x = x
        self._y = y
        self._w = w
        self._h = h    
    
    @property
    def label(self)-> int:
        return self._label 

    @property
    def rect(selft) -> tuple:
        "座標を返す x,y,w,h"
        return (selft._x, selft._y, selft._w, selft._h)