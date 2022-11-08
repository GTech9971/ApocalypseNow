"""
find_contoursにおける輪郭の取得
https://www.learning-nao.com/?p=2020
"""

import cv2


def analyze_contours(contours) -> list:
    # 小さな輪郭は削除する
    new_contours = []
    for i in range(0, len(contours)):
        if len(contours[i]) > 0:

            # remove small objects
            if cv2.contourArea(contours[i]) > 500:
                new_contours.append(contours[i])

    # 一番外側の輪郭は省く
    new_contours = new_contours[1:]
    return new_contours


def exists_point(contour, pt) -> bool:
    ret = cv2.pointPolygonTest(contour, pt, measureDist=False)
    return ret > 0


def save_info(img, contours, hierarchy):
    with open("./result/contours.txt", "w+") as f:
        print(contours, file=f)

    with open("./result/countours_edit.txt", "w") as f:
        print(analyze_contours(contours=contours), file=f)

    with open("./result/hierarchy.txt", "w+") as f:
        print(hierarchy, file=f)

    cv2.imwrite("./result/result.png", img)


# 入力画像
image = cv2.imread('../resources/sample3.png')

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

# 小さい輪郭を削除して文字を消す
new_contours = analyze_contours(contours)

pt = (197, 236)
print(f"Exists:{pt} = {exists_point(contour=new_contours[0], pt=pt)}")

# 輪郭の描画
image_1 = cv2.drawContours(image_copy, new_contours, -1,
                           (0, 255, 0), 2, cv2.LINE_AA)

# ポイントの描画
image_1 = cv2.circle(image_1, pt, 5, (0, 0, 255), -1)
image_1 = cv2.putText(
    image_1, f"x={pt[0]} y={pt[1]}", pt, cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

save_info(image_1, contours, hierarchy)
