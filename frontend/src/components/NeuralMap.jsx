import { useEffect, useRef } from "react";

export default function NeuralMap({ events }) {
const canvasRef = useRef();

useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    let animationFrame;

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const activeEvents = events.slice(0, 50);

        // Ensure positions are computed once per event, then apply motion
        activeEvents.forEach((e) => {
            e.x = e.x ?? Math.random() * canvas.width;
            e.y = e.y ?? Math.random() * canvas.height;

            // random motion
            e.vx = (e.vx || 0) + (Math.random() - 0.5) * 0.2;
            e.vy = (e.vy || 0) + (Math.random() - 0.5) * 0.2;

            // damping (prevents runaway speed)
            e.vx *= 0.95;
            e.vy *= 0.95;

            // update position
            e.x += e.vx;
            e.y += e.vy;

            // soft boundary forces
            const margin = 50;

            if (e.x < margin) e.vx += 0.5;
            if (e.x > canvas.width - margin) e.vx -= 0.5;

            if (e.y < margin) e.vy += 0.5;
            if (e.y > canvas.height - margin) e.vy -= 0.5;

            // hard clamp safety
            e.x = Math.max(0, Math.min(canvas.width, e.x));
            e.y = Math.max(0, Math.min(canvas.height, e.y));
        });

        const hasHighThreat = activeEvents.some(e => e.threat_score > 7);

        // Group events into clusters
        const clusters = {};
        activeEvents.forEach(e => {
            const key = Math.floor(e.threat_score / 3);
            if (!clusters[key]) clusters[key] = [];
            clusters[key].push(e);
        });

        // Draw cluster halos underneath everything
        Object.values(clusters).forEach(cluster => {
            const hasHighThreatInCluster = cluster.some(e => e.threat_score > 7);
            const cx = cluster.reduce((s, e) => s + e.x, 0) / cluster.length;
            const cy = cluster.reduce((s, e) => s + e.y, 0) / cluster.length;

            ctx.beginPath();
            ctx.arc(cx, cy, 20 + cluster.length * 2, 0, 2 * Math.PI);
            
            if (hasHighThreat) {
                if (hasHighThreatInCluster) {
                    ctx.strokeStyle = "rgba(255,50,50,0.8)";
                    ctx.lineWidth = 4;
                } else {
                    ctx.strokeStyle = "rgba(100,0,0,0.1)";
                    ctx.lineWidth = 1;
                }
            } else {
                ctx.strokeStyle = "rgba(255,0,0,0.2)";
                ctx.lineWidth = 2;
            }
            ctx.stroke();
            ctx.lineWidth = 1; // reset for lines
        });

        // Draw connections underneath
        for (let i = 0; i < activeEvents.length; i++) {
            for (let j = i + 1; j < activeEvents.length; j++) {
                const a = activeEvents[i];
                const b = activeEvents[j];

                if (Math.abs(a.threat_score - b.threat_score) < 2) {
                    const isHigh = a.threat_score > 7 || b.threat_score > 7;
                    ctx.beginPath();
                    ctx.moveTo(a.x, a.y);
                    ctx.lineTo(b.x, b.y);
                    
                    if (hasHighThreat) {
                        ctx.strokeStyle = isHigh ? "rgba(255,255,255,0.8)" : "rgba(255,255,255,0.02)";
                    } else {
                        ctx.strokeStyle = "rgba(255,255,255,0.1)";
                    }
                    ctx.stroke();
                }
            }
        }

        // Draw nodes on top
        activeEvents.forEach((e) => {
            const isHigh = e.threat_score > 7;
            const color =
                isHigh
                    ? "red"
                    : e.threat_score > 4
                    ? "yellow"
                    : "green";

            ctx.beginPath();
            let radius = 5 + e.threat_score;
            let alpha = 1.0;
            
            if (hasHighThreat) {
                if (isHigh) {
                    radius *= 1.5; // Draw bigger
                    ctx.shadowBlur = 20; // Brighter glow
                    ctx.shadowColor = "red";
                } else {
                    radius *= 0.8;
                    alpha = 0.2; // Dim others
                    ctx.shadowBlur = 0;
                }
            } else {
                ctx.shadowBlur = 0;
            }

            ctx.arc(e.x, e.y, radius, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.globalAlpha = alpha;
            ctx.fill();
            
            // reset
            ctx.globalAlpha = 1.0;
            ctx.shadowBlur = 0;
        });

        animationFrame = requestAnimationFrame(draw);
    }

    draw();

    return () => cancelAnimationFrame(animationFrame);
}, [events]);

return <canvas ref={canvasRef} className="w-full h-full bg-black" />;

}
