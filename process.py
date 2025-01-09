from image import load_image, detect_faces, save_processed_image  # image.pyから関数をインポート


def process_image(image_path):
    try:
        # 画像を読み込む
        img = load_image(image_path)
        
        # 顔検出を行い、検出結果を画像に描画
        img_with_faces = detect_faces(img)

        # 処理後の画像を保存する
        processed_image_path = save_processed_image(img_with_faces, image_path)

        return processed_image_path

    except ValueError as e:
        # エラーメッセージを返す
        return str(e)
