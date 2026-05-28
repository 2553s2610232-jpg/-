import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pachinko")

html_code = """
<canvas id="gameCanvas" width="500" height="700"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const pegs = [];
const pegRadius = 5;

for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {

        pegs.push({
            x: 80 + col * 45 + (row % 2) * 20,
            y: 120 + row * 45
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

function resetBall() {
    ball.x = 250;
    ball.y = 30;
    ball.vx = (Math.random() - 0.5) * 4;
    ball.vy = 1;
}

resetBall();

function update() {

    ball.vy += 0.2;

    ball.x += ball.vx;
    ball.y += ball.vy;

    // 벽 충돌
    if (ball.x < 10 || ball.x > 490) {
        ball.vx *= -1;
    }

    // 핀 충돌
    pegs.forEach(peg => {

        const dx = ball.x - peg.x;
        const dy = ball.y - peg.y;

        const dist = Math.sqrt(dx*dx + dy*dy);

        if (dist < 15) {
            ball.vx += dx * 0.03;
            ball.vy *= -0.7;
        }
    });

    // 바닥 도달 시 리셋
    if (ball.y > 680) {
        resetBall();
    }
}

function draw() {

    ctx.fillStyle = "#111";
    ctx.fillRect(0,0,500,700);

    // 핀
    ctx.fillStyle = "white";

    pegs.forEach(peg => {
        ctx.beginPath();
        ctx.arc(peg.x, peg.y, pegRadius, 0, Math.PI*2);
        ctx.fill();
    });

    // 공
    ctx.fillStyle = "gold";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);
    ctx.fill();
}

function animate() {
    update();
    draw();
    requestAnimationFrame(animate);
}

animate();

</script>
"""

components.html(html_code, height=720)

st.write("파칭코 게임 실행 중")
