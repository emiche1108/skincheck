import cv2
import os
import numpy as np


# 顔検出用の分類器をロード
def detect_faces(img):
    # Haar Cascade分類器を使って顔検出を行う
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # 画像をグレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 顔を検出する（顔の位置を(x, y, w, h)で返す）
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # 顔が検出されなかった場合、エラーを発生させる
    if len(faces) == 0:
        raise ValueError("顔が検出されませんでした。")

    # 検出した顔に矩形を描画（顔の位置に四角形を描く）
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 顔の情報と、矩形を描画した画像を返す
    return faces, img


# 顔領域を切り出す関数
def extract_face_region(img, faces):
    # 顔の領域をリストに格納
    face_regions = []
    for (x, y, w, h) in faces:
        # 顔領域を切り出す
        face_region = img[y:y+h, x:x+w]
        face_regions.append(face_region)
    # 切り出した顔領域を返す
    return face_regions


# 画像を読み込む関数
def load_image(image_path):
    # OpenCVで画像を読み込み
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError("画像の読み込みに失敗しました。")
    return img


# 結果画像を保存する関数
def save_processed_image(img, original_image_path):
    # 保存先を指定（'static/processed'）
    processed_dir = os.path.join(os.getcwd(), 'static', 'processed')
    # 保存先がない場合、作成する
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    
    # オリジナルの画像パスからファイル名を取得
    base_name = os.path.basename(original_image_path)
    filename, ext = os.path.splitext(base_name)
    
    # 保存先のファイルパスを決定
    processed_image_path = os.path.join(processed_dir, f'{filename}_detected{ext}')
    
    # 画像を保存
    cv2.imwrite(processed_image_path, img)
    
    # 保存した画像のパスを返す
    return processed_image_path


# メイン処理
def process_image(image_path):
    # 画像を読み込む
    img = load_image(image_path)
    
    # 顔検出を行い、顔の位置情報と顔を検出した画像を取得
    faces, detected_img = detect_faces(img)
    
    # 顔領域を切り出す
    face_regions = extract_face_region(detected_img, faces)
    
    # 顔領域に対する処理を追加することができる
    for face_region in face_regions:
        # ここで顔領域に対するさらなる処理（例：肌分析）を実行
        pass
    
    # 処理後の画像を保存
    processed_image_path = save_processed_image(detected_img, image_path)
    
    # 保存された画像のパスを返す
    return processed_image_path
