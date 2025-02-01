import cv2
import os
import numpy as np


def extract_face(image_path, save_path):
    # 画像読み込むみ
    image = cv2.imread(image_path)
    if image is None:
        print(f"画像が見つかりません: {image_path}")
        return None

    # 顔検出用の分類器（Haar Cascade）をロード
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 顔を検出
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # 顔が見つからない場合
    if len(faces) == 0:
        print("顔が検出されませんでした")
        return None
    


    # 最初に検出された顔の座標を取得
    (x, y, w, h) = faces[0]

    # 顔部分だけを切り抜き
    face_region = image[y:y+h, x:x+w]

    # 保存フォルダがなければ作成
    os.makedirs(save_path, exist_ok=True)
    trimmed_path = os.path.join(save_path, "image1_trimmed.png")

    # 画像を保存
    cv2.imwrite(trimmed_path, face_region)
    print(f"顔トリミング成功！保存先: {trimmed_path}")
    
    return trimmed_path

# テスト用（実際にはFlaskアプリから呼び出す）
if __name__ == "__main__":
    input_path = "static/uploads/image1.png"  # 元画像のパス
    output_folder = "static/trimming"  # 保存フォルダ
    extract_face(input_path, output_folder)

