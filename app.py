import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pachinko Game", layout="centered")

st.title("🎰 Streamlit Pachinko")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        overflow: hidden;
        background: #111;
    }

    canvas {
        background: #222;
        display: block;
        margin: auto;
        border: 2px solid white;
    }
</style>
</head>
<body>

<canvas id="gameCanvas" width="500" height="700"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const pegs = [];
const pegRadius = 6;

const rows = 10;
const spacing = 45;

for (let row = 0; row < rows; row++) {
    const cols = row + 3;

    for (let col = 0; col < cols; col++) {
        pegs.push({
            x: 80 + col * spacing - row * spacing / 2,
            y: 100 + row * spacing
        });
    }
}

let ball = {
    x: 250,
    y: 30,
    vx: 0,
    vy: 0,
    radius: 10
};

let gravity = 0.25;
let dropped = false;

function resetBall() {
    ball.x = 250;
    ball.y = 30;
    ball.vx = (Math.random() - 0.5) * 2;
    ball.vy = 0;
    dropped = true;
}

canvas.addEventListener("click", () => {
    if (!dropped) {
        resetBall();
    }
});

function update() {

    if (dropped) {
        ball.vy += gravity;

        ball.x += ball.vx;
        ball.y += ball.vy;

        // 벽 충돌
        if (ball.x < ball.radius || ball.x > canvas.width - ball.radius) {
            ball.vx *= -0.9;
        }

        // 핀 충돌
        pegs.forEach(peg => {
            const dx = ball.x - peg.x;
            const dy = ball.y - peg.y;

            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < ball.radius + pegRadius) {

                // 튕김 방향
                ball.vx += dx * 0.05;
                ball.vy *= -0.7;
            }
        });

        // 바닥 도달
        if (ball.y > canvas.height - 20) {
            dropped = false;
        }
    }
}

function draw() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 핀
    pegs.forEach(peg => {
        ctx.beginPath();
        ctx.arc(peg.x, peg.y, pegRadius, 0, Math.PI * 2);
        ctx.fillStyle = "white";
        ctx.fill();
    });

    // 공
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = "gold";
    ctx.fill();

    // 안내 문구
    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.fillText("Click to Drop Ball", 150, 40);
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();

</script>

</body>
</html>
"""

components.html(html_code, height=720)
