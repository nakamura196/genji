#
# 色抽出のサンプルコード
#
import numpy as np
import cv2
from time import sleep

# メイン関数
def main():
    image = cv2.imread('./test1.png') # ファイル読み込み

    # BGRでの色抽出
    bgrLower = np.array([102, 255, 255])    # 抽出する色の下限
    bgrUpper = np.array([102, 255, 255])    # 抽出する色の上限
    bgrResult = bgrExtraction(image, bgrLower, bgrUpper)
    cv2.imshow('BGR_test1', bgrResult)
    sleep(1)

    # HSVでの色抽出
    hsvLower = np.array([30, 153, 255])    # 抽出する色の下限
    hsvUpper = np.array([30, 153, 255])    # 抽出する色の上限
    hsvResult = hsvExtraction(image, hsvLower, hsvUpper)
    cv2.imshow('HSV_test1', hsvResult)
    sleep(1)

    while True:
        # キー入力を1ms待って、keyが「q」だったらbreak
        key = cv2.waitKey(1)&0xff
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


# BGRで特定の色を抽出する関数
def bgrExtraction(image, bgrLower, bgrUpper):
    img_mask = cv2.inRange(image, bgrLower, bgrUpper) # BGRからマスクを作成
    result = cv2.bitwise_and(image, image, mask=img_mask) # 元画像とマスクを合成
    return result

# HSVで特定の色を抽出する関数
def hsvExtraction(image, hsvLower, hsvUpper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # 画像をHSVに変換
    hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)    # HSVからマスクを作成
    result = cv2.bitwise_and(image, image, mask=hsv_mask) # 元画像とマスクを合成
    return result


if __name__ == '__main__':
    main()