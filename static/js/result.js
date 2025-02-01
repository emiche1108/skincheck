// HTML ドキュメントの読み込みが完了したら実行
document.addEventListener("DOMContentLoaded", function () {
    // 解析対象のファイル名を固定
    const filename = "image1.png";

    // Flask の `/analyze` エンドポイントに POST リクエストを送る
    fetch("/analyze", {
        method: "POST", 
        headers: { "Content-Type": "application/json" },  // JSON データを送るためのヘッダー
        body: JSON.stringify({ filename: filename })  // 送信するデータ（JSON 形式）
    })
    .then(response => response.json())  // サーバーからのレスポンスを JSON に変換
    .then(data => {
        if (data.error) {
            alert(data.error);  
            return;  
        }



        //  解析結果を HTML に表示（Flask からのデータを Web ページに反映）
        // 解析後の画像を `<img>` タグにセット（Flask が返した `processed_image`）
        document.getElementById("processedImage").src = data.processed_image;
        
        // 解析結果
        document.getElementById("brightness").innerText = data.brightness;  // 明るさ
        document.getElementById("oilBalance").innerText = data.oil_balance;  // 皮脂バランス
        document.getElementById("spots").innerText = data.spots;  // シミ
        document.getElementById("wrinkles").innerText = data.wrinkles;  // シワ
        document.getElementById("textureFineness").innerText = data.texture_fineness;  // 肌のキメ細かさ
        document.getElementById("darkCircles").innerText = data.dark_circles;  // くま
        document.getElementById("skinCondition").innerText = data.skin_condition;  // 総合的な肌状態
    })
    .catch(error => console.error("解析エラー:", error));  
});
