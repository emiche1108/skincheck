document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript が正しく読み込まれました！");
    animateCircles(); // アニメーションを手動で実行
});



// ランダムな位置を生成する関数
function getRandomPosition() {
    const x = Math.random() * 40 - 20; // -20px ～ 20px の範囲でランダム移動
    const y = Math.random() * 40 - 20;
    return `translate(${x}px, ${y}px)`;
}

// サークルを動かす関数
function animateCircles() {
    const circles = document.querySelectorAll(".circle");
    circles.forEach(circle => {
        circle.style.transform = getRandomPosition();
    });
}
//0.5秒毎にランダムに動く
setInterval(animateCircles, 500); 


// 10秒後にアニメーションを終了する
setTimeout(() => {
    const loadingScreen = document.getElementById("loading-screen");
    if (loadingScreen) {
        loadingScreen.style.display = "none";
    }

    // 🔥 10秒後に result.html へ遷移
    window.location.href = "/result";
}, 10000); 
