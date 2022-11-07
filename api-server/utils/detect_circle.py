"""
ハフ変換における円の取得
https://self-development.info/opencv%E3%81%A7%E5%86%86%E6%A4%9C%E5%87%BA%E3%82%92%E3%83%8F%E3%83%95%E5%A4%89%E6%8F%9B%E3%81%AB%E3%82%88%E3%82%8A%E8%A1%8C%E3%81%86%E3%80%90houghcircles%E3%80%91/
条件が合わないと使えない
"""

import cv2
import numpy as np

src = cv2.imread("../resources/sample1.png")
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
#gray = cv2.medianBlur(gray, 5)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=70,
                           param1=100, param2=55, minRadius=500, maxRadius=0)


circles = np.uint16(np.around(circles))

for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(src, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(src, (i[0], i[1]), 2, (0, 0, 255), 3)


cv2.imshow('result', src)
cv2.waitKey(0)
cv2.destroyAllWindows()
