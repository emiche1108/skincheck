from flask import Flask, render_template, request, url_for
import os
from werkzeug.utils import secure_filename
from process import process_image  # process.pyから関数をインポート


app = Flask(__name__)

# アップロード先のフォルダを設定
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# アップロード画像の拡張子を設定
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# ファイルの拡張子が、許可されたものか確認する関数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# アップロード先のフォルダが存在しない場合は作成
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)



# トップページ（index.html）にアクセスするルート
@app.route('/')
def home():
    return render_template('index.html')

# 画像アップロードを処理するルート（POSTリクエスト）
@app.route('/upload', methods=['POST'])
def upload_file():
    # ファイルが送信されているか確認
    if 'file' not in request.files:
        return 'ファイルがありません', 400

    file = request.files['file']

    # ファイルが許可された形式か確認
    if file and allowed_file(file.filename):
        # 安全なファイル名に変換
        filename = secure_filename(file.filename)

        # アップロード先のパスを設定
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # ファイルを保存
        file.save(filepath)

        # 画像処理を実行（顔検出）
        processed_image_path = process_image(filepath)  # process.py の関数を呼び出す

        if "顔が検出されませんでした" in processed_image_path:
            return processed_image_path, 400  # エラーメッセージを返す



        # 診断結果（仮の値）
        oil_level = 50  # 油分量（0-100のスケール）
        moisture_level = 30  # 水分量（0-100のスケール）
        texture = 'smooth'  # 肌のテクスチャ（例: smooth, rough）
        redness = 'low'  # 赤み（例: low, medium, high）
        dark_circles = 'none'  # クマの有無（例: none, mild, severe）
        spots = 'mild'  # シミの有無（例: none, mild, moderate, severe）

        # 処理した画像をブラウザで表示する
        return render_template(
            'result.html',
            original_image=url_for('static', filename='uploads/' + filename),
            processed_image=url_for('static', filename='processed/' + f'{filename}_detected.jpg'),
            oil_level=oil_level,
            moisture_level=moisture_level,
            texture=texture,
            redness=redness,
            dark_circles=dark_circles,
            spots=spots
        )

    # 許可されていないファイル形式の場合
    return '不正なファイル形式です', 400


# アプリケーションを起動する部分
if __name__ == '__main__':
    app.run(debug=True)  # デバッグモードでアプリケーションを起動
