document.addEventListener("DOMContentLoaded", function() {
    // HTMLの読み込みが完了した後に実行する
    
    // レーダーチャートを描画するためのコンテキストを取得
    const ctx = document.getElementById('radarChart').getContext('2d');
    
    // レーダーチャートを作成
    new Chart(ctx, {
        type: 'radar', // レーダーチャートの種類を指定
        data: {
            labels: ["ハリ", "キメ", "水分", "油分", "毛穴", "シミ", "シワ", "透明感"], // チャートのラベル（8つの肌診断項目）
            datasets: [{
                label: "スコア", // データセットのラベル
                data: [77, 74, 79, 82, 75, 78, 70, 74], // 各項目のスコアデータ（仮の数値）
                fill: true, // 内部を塗りつぶす
                backgroundColor: "rgba(54, 162, 235, 0.2)", // 塗りつぶしの色（半透明ブルー）
                borderColor: "rgba(54, 162, 235, 1)", // 線の色
                pointBackgroundColor: "rgba(54, 162, 235, 1)" // 各ポイントの色
            }]
        },
        options: {
            responsive: true, // レスポンシブ対応
            scales: {
                r: { // r（半径方向）のスケール設定
                    suggestedMin: 50, // 最小値を50に設定（デフォルト0だと極端な形になりやすい）
                    suggestedMax: 100 // 最大値を100に設定
                }
            }
        }
    });
});
