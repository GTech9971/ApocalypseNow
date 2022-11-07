"""
find_contoursにおける輪郭の取得
https://www.learning-nao.com/?p=2020
"""

import cv2

# 入力画像
image = cv2.imread('../resources/sample1.png')

# 画像のサイズ縮小
height = image.shape[0]
width = image.shape[1]
image = cv2.resize(image, (round(width/4), round(height/4)))

image_copy = image.copy()

# グレースケール化
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 閾値処理
ret, thresh = cv2.threshold(image_gray, 95, 255, cv2.THRESH_BINARY)
cv2.imshow('binary', thresh)


# 輪郭検出 （cv2.RETER_TREE）
contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(f"TREE: {hierarchy}")


# 小さい輪郭を削除して文字を消す
new_contours = []
for i in range(0, len(contours)):
    if len(contours[i]) > 0:

        # remove small objects
        if cv2.contourArea(contours[i]) < 500:
            continue
        else:
            new_contours.append(contours[i])

# 輪郭の描画
image_1 = cv2.drawContours(image_copy, new_contours, -1,
                           (0, 255, 0), 2, cv2.LINE_AA)

# 実行結果
cv2.imshow('cv2.RETR_TREE', image_1)


cv2.imshow('Original', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
