import cv2
import numpy as np


def analyze_skin(face_img_path):
    """切り取った顔画像を解析する"""
    face_img = cv2.imread(face_img_path)
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    
    # 明るさの平均
    mean_brightness = np.mean(gray)

    # 色チャンネルごとの平均値（肌の色バランスを見る）
    b, g, r = cv2.split(face_img)
    mean_red = np.mean(r)
    mean_green = np.mean(g)
    mean_blue = np.mean(b)

    # 肌状態の簡易分析
    skin_condition = "健康"
    if mean_red > mean_blue + 10:
        skin_condition = "赤みが強い"
    elif mean_blue > mean_red + 10:
        skin_condition = "くすみがある"



    # シミの推定（赤くない部分で明るさの違いを分析）
    spots = np.sum((r < 100) & (g < 100) & (b < 100))

    # シワの推定（エッジ検出）
    edges = cv2.Canny(gray, 50, 150)
    wrinkles = np.sum(edges > 0)

    

    # キメの推定（画像のコントラスト）
    texture_fineness = np.var(gray)

    # くまの推定（顔の上半分と下半分の明るさを比較）
    upper_face = np.mean(gray[:gray.shape[0]//2, :])
    lower_face = np.mean(gray[gray.shape[0]//2:, :])
    dark_circles = upper_face - lower_face

    return {
        "brightness": round(mean_brightness, 2),
        "oil_balance": round(mean_blue - mean_red, 2),
        "spots": spots,
        "wrinkles": wrinkles,
        "texture_fineness": round(texture_fineness, 2),
        "dark_circles": round(dark_circles, 2),
        "skin_condition": skin_condition
    }
