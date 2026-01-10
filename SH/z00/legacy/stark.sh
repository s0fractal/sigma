#!/usr/bin/env bash
set -euo pipefail

# s0fractal Visualizer v1.0 (The Stark Interface)
# Generates a Holographic Dashboard with Webcam control.

REPO_ROOT=$(git rev-parse --show-toplevel)
HTML_FILE="$REPO_ROOT/sh/dashboard.html"

echo "🧿 Scanning Void Topology..."

# --- 1. GENERATE STATE JSON ---
JSON_DATA="["
FIRST=1

for DIM in "ts" "rs" "sh" "sigma"; do
  for LAYER in 0 1 2 6 8; do
    PATH="$REPO_ROOT/$DIM/$LAYER"
    if [ -d "$PATH" ]; then
      if [ $FIRST -eq 0 ]; then JSON_DATA+=","; fi

      ENTROPY=$(cd "$PATH" 2>/dev/null && git status --porcelain | wc -l | xargs)
      if [ -z "$ENTROPY" ]; then ENTROPY=0; fi

      JSON_DATA+="{\"name\": \"$DIM-$LAYER\", \"type\": \"$DIM\", \"layer\": $LAYER, \"entropy\": $ENTROPY}"
      FIRST=0
    fi
  done
done
JSON_DATA+="]"

echo "   State captured. Entropy vectors calculated."

# --- 2. GENERATE HTML/JS (The Engine) ---
cat << EOF > "$HTML_FILE"
<!DOCTYPE html>
<html>
<head>
    <title>Σ s0fractal Hologram</title>
    <style>
        body { margin: 0; overflow: hidden; background: #000; font-family: monospace; }
        canvas { display: block; }
        #ui { position: absolute; top: 20px; left: 20px; color: #0f0; pointer-events: none; }
        #video { display: none; }
    </style>
</head>
<body>
    <div id="ui">
        <h1>Σ STATE</h1>
        <div id="stats">Initializing...</div>
        <div id="energy">KINETIC ENERGY: 0%</div>
    </div>
    <video id="video" width="320" height="240" autoplay></video>
    <canvas id="canvas"></canvas>

<script>
const NODES = $JSON_DATA;
const COLORS = {
    ts: '#3388FF', rs: '#FF4433', sh: '#44FF88', sigma: '#CC00FF',
    void: '#FFFFFF', error: '#FF0000'
};

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const video = document.getElementById('video');
let width, height;

function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}
window.onresize = resize;
resize();

let prevFrame = null;
let motionEnergy = 0;

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; })
    .catch(err => console.log("Webcam denied:", err));

function detectMotion() {
    if (video.readyState !== 4) return 0;

    const w = 64, h = 48;
    const buffer = document.createElement('canvas');
    buffer.width = w; buffer.height = h;
    const bctx = buffer.getContext('2d');

    bctx.drawImage(video, 0, 0, w, h);
    const frame = bctx.getImageData(0, 0, w, h).data;

    let diff = 0;
    if (prevFrame) {
        for (let i = 0; i < frame.length; i += 4) {
            const l1 = (frame[i] + frame[i+1] + frame[i+2]) / 3;
            const l2 = (prevFrame[i] + prevFrame[i+1] + prevFrame[i+2]) / 3;
            diff += Math.abs(l1 - l2);
        }
    }
    prevFrame = frame;
    return diff / (w * h * 255);
}

class Particle {
    constructor(node) {
        this.node = node;
        this.angle = Math.random() * Math.PI * 2;
        this.radius = 100 + (node.layer * 40);
        this.baseColor = COLORS[node.type] || COLORS.void;
        this.size = 3 + (node.entropy * 2);
    }

    update(energy) {
        let speed = 0.005 + (energy * 0.05);
        if (this.node.entropy > 0) speed *= 0.5;

        this.angle += speed;
        this.wobble = (this.node.entropy > 0) ? Math.sin(Date.now() * 0.01) * 10 : 0;
    }

    draw(ctx, cx, cy) {
        const x = cx + Math.cos(this.angle) * (this.radius + this.wobble);
        const y = cy + Math.sin(this.angle) * (this.radius + this.wobble);
        const scale = 0.5 + (Math.sin(this.angle) + 1) / 2;

        ctx.beginPath();
        ctx.arc(x, y, this.size * scale, 0, Math.PI * 2);
        ctx.fillStyle = this.node.entropy > 0 ? COLORS.error : this.baseColor;

        if (motionEnergy > 0.5) {
            ctx.shadowBlur = 10;
            ctx.shadowColor = ctx.fillStyle;
        } else {
            ctx.shadowBlur = 0;
        }

        ctx.fill();

        if (scale > 0.8) {
            ctx.fillStyle = '#fff';
            ctx.font = '10px monospace';
            ctx.fillText(this.node.name, x + 10, y);
        }
    }
}

const particles = NODES.map(n => new Particle(n));

function animate() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.fillRect(0, 0, width, height);

    const input = detectMotion();
    motionEnergy = motionEnergy * 0.9 + input * 0.5;
    document.getElementById('energy').innerText = \`ENERGY: \${Math.floor(motionEnergy * 100)}%\`;

    const cx = width / 2;
    const cy = height / 2;

    ctx.beginPath();
    ctx.arc(cx, cy, 10 + (motionEnergy * 20), 0, Math.PI * 2);
    ctx.strokeStyle = '#333';
    ctx.stroke();

    particles.forEach(p => {
        p.update(motionEnergy);
        p.draw(ctx, cx, cy);
    });

    requestAnimationFrame(animate);
}

animate();
</script>
</body>
</html>
EOF

echo "✅ Hologram generated at $HTML_FILE"
echo "🚀 Launching Interface..."

open "$HTML_FILE" 2>/dev/null || xdg-open "$HTML_FILE" 2>/dev/null || echo "Open sh/dashboard.html manually."
