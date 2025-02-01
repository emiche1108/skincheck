from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, abort, jsonify
import os
import base64  # 写真撮影。Base64エンコードとデコードを行う
import cv2
from urllib.parse import quote, unquote # 写真撮影時のURLエンコードのために追加
from session import save_survey_data, get_survey_data  # アンケートの保存
from urllib.parse import unquote  # 結果ページのURLデコード用
from process import detect_faces, extract_face_region
from image_processing import extract_face  # 顔の切り取り
import numpy as np



# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__, static_folder="static", template_folder="templates")

app.secret_key = os.urandom(24)  # 管理用の秘密鍵

# 保存先フォルダ
UPLOAD_FOLDER = "static/uploads"
TRIM_FOLDER = "static/trimming"
PROCESSED_FOLDER = "static/processed"

for folder in [UPLOAD_FOLDER, TRIM_FOLDER, PROCESSED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRIM_FOLDER'] = TRIM_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

FILENAME = "image1.png"


# 許可するファイル形式（拡張子）の設定
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# ファイル拡張子の確認
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 保存時のファイル名（固定）
FILENAME = "image1.png"



# 顔認識学習済み情報の読み込み
@app.route('/models/weights/<filename>')
def serve_models(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/models/weights'), filename)



# トップページ（index.html）→アンケートページ（skinQ.html）へ
@app.route('/')
def home():
    return render_template('index.html')



# アンケートページ（skinQ.html）→選択ページ（choose _image.html）へ
@app.route('/skinQ', methods=['GET', 'POST'])
def skinQ():
    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        skin_issues = request.form.getlist('skin_issues') or ['なし']

        # アンケート結果を保存
        save_survey_data(age, gender, skin_issues)

        # 次のページ（画像選択ページ）へリダイレクト
        return redirect(url_for('choose_image'))
    
    return render_template('skinQ.html')



# 選択ページ（choose_image.html）
@app.route('/choose_image')
def choose_image():
    return render_template('choose_image.html')



# 画像保存先の宣言
def save_image(photo_data):
    filepath = os.path.join(UPLOAD_FOLDER, FILENAME)
    
    try:
        with open(filepath, 'wb') as f:
            f.write(photo_data)
        print(f"✅ 画像保存成功: {filepath}")
        return filepath  # 保存したファイルのパスを返す
    
    except Exception as e:
        print(f"❌ 画像保存エラー: {e}")
        abort(500, "画像保存に失敗しました")



# ...カメラ起動とトリミング
@app.route('/take_photo_page', methods=['GET', 'POST'])
def take_photo_page():
    if request.method == 'GET':
        return render_template('take_photo.html')

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "データが送信されていません"}), 400

        photo_data = data.get("photoData", "")
        if not photo_data:
            return jsonify({"error": "photoData が空です"}), 400

        # 画像をデコードし、保存
        photo_data = base64.b64decode(photo_data.replace("data:image/png;base64,", ""))
        filepath = save_image(photo_data)

        # 📌 顔部分のトリミング処理
        trimmed_path = os.path.join(TRIM_FOLDER, FILENAME)
        try:
            face_region = extract_face(filepath)

            # ✅ face_region が正しく取得できたかチェック
            if face_region is None or not isinstance(face_region, np.ndarray):
                raise ValueError("顔のトリミングに失敗しました。")

            cv2.imwrite(trimmed_path, face_region)
            print(f"✨ トリミング完了: {trimmed_path}")

            # `processed/` にコピー
            processed_path = os.path.join(PROCESSED_FOLDER, FILENAME)
            cv2.imwrite(processed_path, face_region)
            print(f"✅ 処理済み画像を保存: {processed_path}")

        except Exception as e:
            print(f"❌ トリミングエラー: {e}")

        return render_template("animation.html")

    except Exception as e:
        print(f"❌ エラー: {e}")
        return jsonify({"error": "サーバー内部エラー"}), 500




# ...画像アップロードとトリミング
@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo_page():
    if request.method == 'GET':
        return render_template('upload_photo.html')

    if 'file' not in request.files:
        abort(400, "エラー: ファイルが送信されていません")

    file = request.files['file']
    if file.filename == '':
        abort(400, "エラー: ファイルが選択されていません")

    filepath = save_image(file.read())

    # 📌 トリミング処理
    trimmed_path = os.path.join(TRIM_FOLDER, FILENAME)
    try:
        face_region = extract_face(filepath)

        # ✅ face_region が正しく取得できたかチェック
        if face_region is None or not isinstance(face_region, np.ndarray):
            raise ValueError("顔のトリミングに失敗しました。")

        cv2.imwrite(trimmed_path, face_region)
        print(f"✨ トリミング完了: {trimmed_path}")

        # `processed/` にコピー
        processed_path = os.path.join(PROCESSED_FOLDER, FILENAME)
        cv2.imwrite(processed_path, face_region)
        print(f"✅ 処理済み画像を保存: {processed_path}")

    except Exception as e:
        print(f"❌ トリミングエラー: {e}")

    return render_template("animation.html")




# 解析
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        trimmed_path = os.path.join(TRIM_FOLDER, FILENAME)
        processed_path = os.path.join(PROCESSED_FOLDER, FILENAME)

        if not os.path.exists(trimmed_path):
            return jsonify({"error": "トリミング画像が見つかりません"}), 404

        return jsonify({
            "trimmed_image": f"/static/trimming/{FILENAME}",
            "processed_image": f"/static/processed/{FILENAME}",
            "message": "顔の切り取り成功"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# アニメーション
@app.route('/animation')
def start_animation():
    print("🎬 アニメーションページを表示")  
    return render_template('animation.html')  
 


# 結果ページ
@app.route('/result')
def result():
    filename = "image1.png"  #  解析する画像は常にこれ
    trimmed_path = os.path.join(TRIM_FOLDER, filename)  
    processed_path = os.path.join(PROCESSED_FOLDER, filename)

    # 🔍 トリミング画像が存在するかチェック
    if not os.path.exists(trimmed_path):
        print(f"❌ トリミング画像が見つかりません: {trimmed_path}")
        return abort(404, "トリミング画像が見つかりません")

    return render_template(
        'result.html',
        original_image=url_for('static', filename=f'uploads/{filename}'),
        trimmed_image=url_for('static', filename=f'trimming/{filename}'),
        processed_image=url_for('static', filename=f'processed/{filename}')
    )




if __name__ == '__main__':
    app.run(debug=True)
    