import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pachinko Casino", layout="centered")

st.title("🎰 Pachinko Casino")

balance = st.number_input("현재 보유 코인", value=1000)

bet = st.slider("배팅 금액", 10, 500, 50)

ball_count = st.slider("공 개수", 1, 20, 5)

st.write(f"총 배팅: {bet * ball_count} 코인")

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin:0;
    background:#111;
}}

canvas {{
    display:block;
    margin:auto;
    background:#1b1b1b;
    border:3px solid white;
}}
</style>
</head>
<body>

<canvas id="gameCanvas" width="500" height="750"></canvas>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const WIDTH = 500;
const HEIGHT = 750;

const pegRadius = 5;
const pegs = [];

const rows = 10;
const spacing = 45;

// 핀 생성
for(let row=0; row<rows; row++) {{

    for(let col=0; col<10; col++) {{

        pegs.push({{
            x: 60 + col * spacing + (row % 2) * 20,
            y: 100 + row * spacing
        }});
    }}
}}

// 슬롯 배당
const multipliers = [0, 0.5, 1, 2, 5, 10, 5, 2, 1, 0.5];

const slotWidth = WIDTH / multipliers.length;

const balls = [];

function createBall() {{

    balls.push({{
        x: 250 + (Math.random()-0.5)*50,
        y: 20,
        vx: (Math.random()-0.5)*2,
        vy: 0,
        radius: 8,
        active: true
    }});
}}

for(let i=0; i<{ball_count}; i++) {{
    setTimeout(createBall, i * 300);
}}

function updateBall(ball) {{

    if(!ball.active) return;

    ball.vy += 0.2;

    ball.x += ball.vx;
    ball.y += ball.vy;

    // 벽
    if(ball.x < ball.radius || ball.x > WIDTH-ball.radius) {{
        ball.vx *= -1;
    }}

    // 핀 충돌
    pegs.forEach(peg => {{

        const dx = ball.x - peg.x;
        const dy = ball.y - peg.y;

        const dist = Math.sqrt(dx*dx + dy*dy);

        if(dist < ball.radius + pegRadius) {{

            ball.vx += dx * 0.03;

            ball.vy *= -0.75;
        }}
    }});

    // 바닥
    if(ball.y > HEIGHT - 60) {{

        ball.active = false;

        const slot = Math.floor(ball.x / slotWidth);

        const multiplier = multipliers[slot];

        ball.reward = multiplier * {bet};

        console.log("획득:", ball.reward);
    }}
}}

function drawBoard() {{

    ctx.fillStyle = "#111";
    ctx.fillRect(0,0,WIDTH,HEIGHT);

    // 핀
    ctx.fillStyle = "white";

    pegs.forEach(peg => {{
        ctx.beginPath();
        ctx.arc(peg.x, peg.y, pegRadius, 0, Math.PI*2);
        ctx.fill();
    }});

    // 슬롯
    for(let i=0; i<multipliers.length; i++) {{

        ctx.fillStyle = i % 2 == 0 ? "#333" : "#444";

        ctx.fillRect(i*slotWidth, HEIGHT-50, slotWidth, 50);

        ctx.fillStyle = "gold";
        ctx.font = "18px Arial";

        ctx.fillText(
            multipliers[i] + "x",
            i*slotWidth + 10,
            HEIGHT-20
        );
    }}
}}

function drawBalls() {{

    balls.forEach(ball => {{

        ctx.beginPath();

        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);

        ctx.fillStyle = ball.active ? "gold" : "lime";

        ctx.fill();
    }});
}}

function animate() {{

    drawBoard();

    balls.forEach(updateBall);

    drawBalls();

    requestAnimationFrame(animate);
}}

animate();

</script>

</body>
</html>
"""

components.html(html_code, height=760)
