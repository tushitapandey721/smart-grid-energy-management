/**
 * VoltIQ Interactive Electric Wave & Particle Silk Canvas Engine
 * Generates smooth, luminous electric current waves and responding grid energy particles.
 */

class ElectricWaveCanvas {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width = this.canvas.offsetWidth || window.innerWidth;
        this.height = this.canvas.height = this.canvas.offsetHeight || window.innerHeight;
        
        this.mouse = {
            x: this.width / 2,
            y: this.height / 2,
            targetX: this.width / 2,
            targetY: this.height / 2,
            isHovered: false
        };

        this.time = 0;
        this.waves = [
            { amplitude: 45, frequency: 0.008, speed: 0.02, color: 'rgba(56, 189, 248, 0.45)', lineWidth: 2.5, phase: 0 },
            { amplitude: 35, frequency: 0.012, speed: 0.03, color: 'rgba(0, 242, 254, 0.55)', lineWidth: 2.0, phase: 2 },
            { amplitude: 55, frequency: 0.006, speed: 0.015, color: 'rgba(16, 185, 129, 0.4)', lineWidth: 2.0, phase: 4 },
            { amplitude: 25, frequency: 0.018, speed: 0.025, color: 'rgba(99, 102, 241, 0.35)', lineWidth: 1.5, phase: 1 },
            { amplitude: 60, frequency: 0.005, speed: 0.018, color: 'rgba(56, 189, 248, 0.25)', lineWidth: 3.0, phase: 3 }
        ];

        // Electric discharge particles
        this.particles = [];
        this.particleCount = 45;
        this.initParticles();

        this.bindEvents();
        this.animate();
    }

    initParticles() {
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.width,
                y: Math.random() * this.height,
                radius: Math.random() * 2 + 1,
                vx: (Math.random() - 0.5) * 0.8,
                vy: (Math.random() - 0.5) * 0.8,
                alpha: Math.random() * 0.7 + 0.3,
                color: Math.random() > 0.4 ? '#00f2fe' : '#10b981',
                orbitRadius: Math.random() * 80 + 20,
                orbitAngle: Math.random() * Math.PI * 2,
                orbitSpeed: (Math.random() - 0.5) * 0.02
            });
        }
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            if (!this.canvas) return;
            this.width = this.canvas.width = this.canvas.offsetWidth || window.innerWidth;
            this.height = this.canvas.height = this.canvas.offsetHeight || window.innerHeight;
            this.initParticles();
        });

        window.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.targetX = e.clientX - rect.left;
            this.mouse.targetY = e.clientY - rect.top;
            this.mouse.isHovered = true;
        });

        window.addEventListener('mouseleave', () => {
            this.mouse.isHovered = false;
        });
    }

    drawWaves() {
        const ctx = this.ctx;
        this.time += 1;

        // Smooth mouse interpolation
        this.mouse.x += (this.mouse.targetX - this.mouse.x) * 0.05;
        this.mouse.y += (this.mouse.targetY - this.mouse.y) * 0.05;

        this.waves.forEach((wave, idx) => {
            ctx.beginPath();
            ctx.lineWidth = wave.lineWidth;
            ctx.strokeStyle = wave.color;
            ctx.shadowColor = wave.color;
            ctx.shadowBlur = 12;

            const baseHeight = (this.height * 0.5) + (idx - 2) * 20;

            for (let x = 0; x <= this.width; x += 6) {
                // Distance to mouse for interactive electric deflection
                const dx = x - this.mouse.x;
                const dy = baseHeight - this.mouse.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                const mouseInfluence = Math.max(0, 1 - dist / 220) * 45;

                const sinFactor = Math.sin(x * wave.frequency + this.time * wave.speed + wave.phase);
                const cosFactor = Math.cos(x * (wave.frequency * 0.5) + this.time * (wave.speed * 0.7));
                const y = baseHeight + (sinFactor * wave.amplitude) + (cosFactor * 15) - (mouseInfluence * Math.sin(this.time * 0.05));

                if (x === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            ctx.stroke();
            ctx.shadowBlur = 0; // Reset
        });
    }

    drawParticles() {
        const ctx = this.ctx;
        this.particles.forEach(p => {
            // Move along trajectory with slight mouse attraction
            p.x += p.vx;
            p.y += p.vy;

            // Wrap around edges
            if (p.x < 0) p.x = this.width;
            if (p.x > this.width) p.x = 0;
            if (p.y < 0) p.y = this.height;
            if (p.y > this.height) p.y = 0;

            // Glow point
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowColor = p.color;
            ctx.shadowBlur = 8;
            ctx.globalAlpha = p.alpha;
            ctx.fill();
            ctx.globalAlpha = 1.0;
            ctx.shadowBlur = 0;
        });

        // Draw connections between nearby particles (Energy Net)
        ctx.lineWidth = 0.5;
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 90) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(0, 242, 254, ${0.25 * (1 - dist / 90)})`;
                    ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    ctx.stroke();
                }
            }
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.width, this.height);
        this.drawWaves();
        this.drawParticles();
        requestAnimationFrame(() => this.animate());
    }
}

// 3D Card Tilt Engine
function init3DTilt() {
    const cards = document.querySelectorAll('[data-tilt]');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -8;
            const rotateY = ((x - centerX) / centerX) * 8;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    new ElectricWaveCanvas('heroWaveCanvas');
    new ElectricWaveCanvas('bgSilkCanvas');
    init3DTilt();
});
