import cv2
import numpy as np
import matplotlib.pyplot as plt


# 2値化
def calc_threshold(gray_img):
    luminance_percentage = 0.2
    num_threshold = gray_img.size * luminance_percentage
    flat = gray_img.flatten()

    for diff_luminance in range(100):
        if np.count_nonzero(flat > 200 - diff_luminance) >= num_threshold:
            return 200 - diff_luminance
    return 100


# 輪郭取得
def draw_countour_extraction(binary_img, drawed_img):
    contours, _ = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key=cv2.contourArea)
    line_color = (0, 255, 0)
    thickness = 30
    cv2.drawContours(drawed_img, [cnt], -1, line_color, thickness)

    return cnt


# 画像の射影変換
def transform(img_width: int, img_height: int, cnt):
    epsilon = 0.1 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    src = np.float32(list(map(lambda x: x[0], approx)))
    dst = np.float32([[0, 0], [0, img_width], [img_height, img_width], [img_height, 0]])

    project_matrix = cv2.getPerspectiveTransform(src, dst)

    # 先ほどで線が上書きされたので再度画像を取得
    img = cv2.imread('resources/img_cut.png')
    transformed = cv2.warpPerspective(img, project_matrix, (img_height, img_width))
    plt.imshow(cv2.cvtColor(transformed, cv2.COLOR_BGR2RGB))
    plt.show()


def main():
    # load img
    img = cv2.imread('resources/img_cut.png')
    # グレイスケール
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold = calc_threshold(gray_img)
    print(f"threshold:{threshold}")

    # 2値化
    _, binary_img = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)

    # 輪郭抽出
    cnt = draw_countour_extraction(binary_img, img)
    dst_img = img
    plt.imshow(cv2.cvtColor(dst_img, cv2.COLOR_BGR2RGB))
    plt.show()

    width, height, _ = dst_img.shape
    transform(width, height, cnt)


if __name__ == '__main__':
    main()
