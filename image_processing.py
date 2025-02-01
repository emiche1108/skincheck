import cv2
import numpy as np



def extract_face(image_path):
    """
    画像から顔部分を切り抜く関数
    :param image_path: 画像のパス
    :return: 顔部分の画像（numpy 配列）or None
    """
    # 画像を読み込む
    image = cv2.imread(image_path)

    if image is None:
        print(f"❌ 画像の読み込みに失敗しました: {image_path}")
        return None  # 画像が読み込めなかった場合は `None` を返す

    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Haar Cascade の分類器をロード
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # 顔を検出
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # 顔が検出されなかった場合のエラーハンドリング
    if len(faces) == 0:
        print("❌ 顔が検出されませんでした")
        return None

    # 最初の顔の座標を取得
    x, y, w, h = faces[0]

    # 顔部分だけを切り抜き
    face_region = image[y:y+h, x:x+w]

    # ✅ 画像データが `numpy.ndarray` かどうかを確認
    if not isinstance(face_region, np.ndarray):
        print("❌ トリミング後のデータが無効です")
        return None

    return face_region
