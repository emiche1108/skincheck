import cv2
import os
import numpy as np


# 画像を読み込む
def load_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("画像の読み込みに失敗しました。")
    return img


# 顔検出用の分類器をロード
def detect_faces(img):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 顔検出
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        raise ValueError("顔が検出されませんでした。")

    # 検出した顔に矩形を描画
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return faces, img


# 顔領域を切り出す関数
def extract_face_region(img, faces):
    face_regions = []
    for (x, y, w, h) in faces:
        face_region = img[y:y+h, x:x+w]
        face_regions.append(face_region)
    return face_regions


# 輝度マップの計測
def calculate_brightness(face_region):
    gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)  # 輝度の平均
    return mean_brightness


# HSV色空間を使って色調の分析
def analyze_color_tone(face_region):
    # BGR -> HSV
    hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)
    
    # H: 色相, S: 彩度, V: 明度
    h, s, v = cv2.split(hsv)
    
    mean_hue = np.mean(h)  # 色相の平均
    mean_saturation = np.mean(s)  # 彩度の平均
    mean_value = np.mean(v)  # 明度の平均
    
    return mean_hue, mean_saturation, mean_value


# 水分量や油分量を推測
def estimate_skin_condition(face_region):
    # 輝度を計算
    brightness = calculate_brightness(face_region)
    
    # 色調を分析
    mean_hue, mean_saturation, mean_value = analyze_color_tone(face_region)
    
    # 水分量と油分量の推測
    if brightness > 150 and mean_hue > 20 and mean_hue < 40:
        # 高輝度 + 黄色味が強い => 油分が多い
        skin_condition = "油分が多い"
    elif brightness < 100 and mean_hue > 5 and mean_hue < 20:
        # 低輝度 + 赤みが強い => 乾燥している
        skin_condition = "乾燥している"
    else:
        # 通常の肌状態
        skin_condition = "正常な肌状態"
    
    return skin_condition, brightness, mean_hue, mean_saturation, mean_value


# 肌の状態を分析する関数（輝度、色調などを簡易的に分析）
def analyze_skin_condition(face_region):
    # グレースケールに変換
    gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
    mean_brightness = gray.mean()
    
    # RGBカラーの平均値を計算する。
    b, g, r = cv2.split(face_region)
    mean_red = r.mean()
    mean_green = g.mean()
    mean_blue = b.mean()
    
    # 赤みや乾燥を簡易的に判定
    if mean_red > mean_blue and mean_red > mean_green:
        skin_condition = "赤みが強い (乾燥か刺激)"
    else:
        skin_condition = "正常な肌状態"
    
    return skin_condition, mean_brightness, mean_red, mean_green, mean_blue


# 結果画像を保存する関数
def save_processed_image(img, original_image_path):
    processed_dir = os.path.join(os.getcwd(), 'static', 'processed')
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    base_name = os.path.basename(original_image_path)
    filename, ext = os.path.splitext(base_name)
    processed_image_path = os.path.join(processed_dir, f'{filename}_detected{ext}')
    # 結果を保存
    cv2.imwrite(processed_image_path, img)
    return processed_image_path


# メイン処理
def process_image(image_path):
    # 画像を読み込む
    img = load_image(image_path)
    
    # 顔検出
    faces, detected_img = detect_faces(img)
    
    # 顔領域を切り出す
    face_regions = extract_face_region(detected_img, faces)
    
    # 顔領域ごとに分析
    for face_region in face_regions:
        # 肌の状態を分析
        skin_condition, brightness, red, green, blue = analyze_skin_condition(face_region)
        
        # 水分量と油分量の推測
        estimated_condition, est_brightness, est_hue, est_saturation, est_value = estimate_skin_condition(face_region)
        
        print(f"肌状態: {skin_condition}, 輝度: {brightness}, 赤み: {red}, 緑: {green}, 青: {blue}")
        print(f"推測: {estimated_condition}, 輝度: {est_brightness}, 色相: {est_hue}, 彩度: {est_saturation}, 明度: {est_value}")
    

    
    # 結果画像を保存
    processed_image_path = save_processed_image(detected_img, image_path)
    return processed_image_path
