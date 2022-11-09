class HitPoint(object):
    """
    ヒットした座標
    """

    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def point(self) -> tuple:
        return (self.__x, self.__y)
