/**
 * Smart Grid Energy Management - Client Controller
 * Handles live telemetry, gauge rendering, Chart.js graphs, AJAX prediction & animations.
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- State & Chart Instances ---
    let donutChartInstance = null;
    let lineChartInstance = null;
    let targetKw = 1.85;
    let currentKw = 0;

    // --- DOM Elements ---
    const liveClockEl = document.getElementById('liveClock');
    const btnUseCurrentTime = document.getElementById('btnUseCurrentTime');
    const customDatetimeInput = document.getElementById('custom_datetime');
    const predictionForm = document.getElementById('predictionForm');
    const btnSubmit = document.getElementById('btnSubmit');
    const presetPills = document.querySelectorAll('.preset-btn');
    const gaugeCanvas = document.getElementById('gaugeCanvas');
    const predValueEl = document.getElementById('predValue');
    const tierBadge = document.getElementById('tierBadge');
    const tierLabel = document.getElementById('tierLabel');
    const tierAdviceText = document.getElementById('tierAdviceText');

    // Financial & Metric Readouts
    const valCostUsd = document.getElementById('valCostUsd');
    const valCostInr = document.getElementById('valCostInr');
    const valMonthKwh = document.getElementById('valMonthKwh');
    const valMonthCost = document.getElementById('valMonthCost');
    const valCarbon = document.getElementById('valCarbon');
    const valPeakStatus = document.getElementById('valPeakStatus');
    const recText = document.getElementById('recText');

    // 1. Live Grid Clock
    function updateLiveClock() {
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        if (liveClockEl) liveClockEl.textContent = timeStr;
    }
    setInterval(updateLiveClock, 1000);
    updateLiveClock();

    // 2. Synchronize Local Datetime & Auto-derive features
    function setFormToDatetime(dateObj) {
        const localISO = new Date(dateObj.getTime() - dateObj.getTimezoneOffset() * 60000)
            .toISOString()
            .slice(0, 16);
        if (customDatetimeInput) customDatetimeInput.value = localISO;

        const hour = dateObj.getHours();
        const day = dateObj.getDate();
        const month = dateObj.getMonth() + 1;
        const year = dateObj.getFullYear();
        const jsWeekday = dateObj.getDay(); // 0 is Sun, 1 is Mon...
        // Convert to python weekday (0 is Mon, 6 is Sun)
        const pyWeekday = (jsWeekday + 6) % 7;
        const isWeekend = (pyWeekday === 5 || pyWeekday === 6) ? 1 : 0;
        const isPeak = (hour >= 18 && hour <= 22) ? 1 : 0;

        // Set inputs
        const setVal = (id, v) => {
            const el = document.getElementById(id);
            if (el) el.value = v;
        };

        setVal('Hour', hour);
        setVal('Day', day);
        setVal('Month', month);
        setVal('Year', year);
        setVal('Weekday', pyWeekday);
        setVal('Weekend', isWeekend);
        setVal('Peak_Hour', isPeak);

        if (valPeakStatus) {
            valPeakStatus.textContent = isPeak === 1 ? 'PEAK TARIFF' : 'OFF-PEAK';
        }
    }

    // Default datetime on load
    setFormToDatetime(new Date());

    if (btnUseCurrentTime) {
        btnUseCurrentTime.addEventListener('click', () => {
            setFormToDatetime(new Date());
            triggerPrediction();
        });
    }

    if (customDatetimeInput) {
        customDatetimeInput.addEventListener('change', (e) => {
            if (e.target.value) {
                setFormToDatetime(new Date(e.target.value));
            }
        });
    }

    // 3. Scenario Presets Handler
    presetPills.forEach(btn => {
        btn.addEventListener('click', () => {
            presetPills.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const presetKey = btn.getAttribute('data-preset');
            if (window.PRESETS_DATA && window.PRESETS_DATA[presetKey]) {
                const pData = window.PRESETS_DATA[presetKey].data;
                Object.keys(pData).forEach(k => {
                    const inputEl = document.getElementById(k);
                    if (inputEl) inputEl.value = pData[k];
                });
                
                // Trigger live inference
                triggerPrediction();
            }
        });
    });

    // 4. Canvas-based Animated Radial Gauge
    function drawGauge(val) {
        if (!gaugeCanvas) return;
        const ctx = gaugeCanvas.getContext('2d');
        const width = gaugeCanvas.width;
        const height = gaugeCanvas.height;
        const cx = width / 2;
        const cy = height - 20;
        const radius = 95;

        ctx.clearRect(0, 0, width, height);

        // Background Arc (Gray track)
        ctx.beginPath();
        ctx.arc(cx, cy, radius, Math.PI, 2 * Math.PI, false);
        ctx.lineWidth = 14;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
        ctx.lineCap = 'round';
        ctx.stroke();

        // Calculate progress angle (0 to 6 kW scale)
        const maxKw = 6.0;
        const clampedVal = Math.min(Math.max(val, 0), maxKw);
        const ratio = clampedVal / maxKw;
        const endAngle = Math.PI + (ratio * Math.PI);

        // Active Arc Gradient
        const gradient = ctx.createLinearGradient(20, cy, width - 20, cy);
        gradient.addColorStop(0, '#10b981');   // Eco Green
        gradient.addColorStop(0.5, '#00f2fe'); // Electric Cyan
        gradient.addColorStop(0.8, '#f59e0b'); // Warning Amber
        gradient.addColorStop(1, '#ef4444');   // Peak Red

        if (ratio > 0.01) {
            ctx.beginPath();
            ctx.arc(cx, cy, radius, Math.PI, endAngle, false);
            ctx.lineWidth = 14;
            ctx.strokeStyle = gradient;
            ctx.lineCap = 'round';
            ctx.shadowColor = ratio > 0.6 ? 'rgba(239, 68, 68, 0.6)' : 'rgba(0, 242, 254, 0.5)';
            ctx.shadowBlur = 15;
            ctx.stroke();
            ctx.shadowBlur = 0; // Reset shadow
        }

        // Ticks
        for (let i = 0; i <= 6; i++) {
            const angle = Math.PI + (i / 6) * Math.PI;
            const innerR = radius - 16;
            const outerR = radius - 10;
            const x1 = cx + innerR * Math.cos(angle);
            const y1 = cy + innerR * Math.sin(angle);
            const x2 = cx + outerR * Math.cos(angle);
            const y2 = cy + outerR * Math.sin(angle);

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.lineWidth = 2;
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
            ctx.stroke();
        }
    }

    // Number count-up animation loop
    function animateGaugeTo(val) {
        targetKw = val;
        const step = () => {
            const diff = targetKw - currentKw;
            if (Math.abs(diff) > 0.01) {
                currentKw += diff * 0.15;
                if (predValueEl) predValueEl.textContent = currentKw.toFixed(3);
                drawGauge(currentKw);
                requestAnimationFrame(step);
            } else {
                currentKw = targetKw;
                if (predValueEl) predValueEl.textContent = currentKw.toFixed(3);
                drawGauge(currentKw);
            }
        };
        requestAnimationFrame(step);
    }

    // 5. Chart.js Graphs Initialization & Updates
    function initCharts(breakdown, simulated24h) {
        // A. Donut Chart (Sub-metering Distribution)
        const donutCtx = document.getElementById('applianceDonutChart');
        if (donutCtx) {
            const donutData = {
                labels: ['Kitchen (Sub 1)', 'Laundry (Sub 2)', 'HVAC / Water Heat (Sub 3)', 'Baseline Load'],
                datasets: [{
                    data: [
                        breakdown.kitchen_pct,
                        breakdown.laundry_pct,
                        breakdown.hvac_pct,
                        breakdown.base_pct
                    ],
                    backgroundColor: [
                        '#38bdf8', // Blue
                        '#a855f7', // Purple
                        '#f59e0b', // Amber
                        '#10b981'  // Green
                    ],
                    borderColor: '#0f172a',
                    borderWidth: 3,
                    hoverOffset: 6
                }]
            };

            if (donutChartInstance) {
                donutChartInstance.data = donutData;
                donutChartInstance.update();
            } else {
                donutChartInstance = new Chart(donutCtx, {
                    type: 'doughnut',
                    data: donutData,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '68%',
                        plugins: {
                            legend: {
                                position: 'right',
                                labels: {
                                    color: '#94a3b8',
                                    font: { family: 'Inter', size: 11 },
                                    boxWidth: 12,
                                    padding: 10
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function (context) {
                                        return ` ${context.label}: ${context.raw}%`;
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }

        // B. Line Chart (24-Hour Load Curve)
        const lineCtx = document.getElementById('dailyLoadLineChart');
        if (lineCtx) {
            const hoursLabels = Array.from({ length: 24 }, (_, i) => `${i}:00`);
            const lineData = {
                labels: hoursLabels,
                datasets: [{
                    label: 'Simulated Load (kW)',
                    data: simulated24h,
                    fill: true,
                    backgroundColor: 'rgba(0, 242, 254, 0.1)',
                    borderColor: '#00f2fe',
                    borderWidth: 2,
                    tension: 0.4,
                    pointRadius: 2,
                    pointHoverRadius: 5,
                    pointBackgroundColor: '#00f2fe'
                }]
            };

            if (lineChartInstance) {
                lineChartInstance.data = lineData;
                lineChartInstance.update();
            } else {
                lineChartInstance = new Chart(lineCtx, {
                    type: 'line',
                    data: lineData,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: {
                                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                                ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 8 }
                            },
                            y: {
                                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                                ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } },
                                suggestedMin: 0,
                                suggestedMax: 5
                            }
                        },
                        plugins: {
                            legend: { display: false }
                        }
                    }
                });
            }
        }
    }

    // 6. Update UI with Prediction Analytics
    function updateAnalyticsUI(data) {
        if (!data) return;

        // Animate Gauge
        animateGaugeTo(data.predicted_kw);

        // Update Tier Badge
        if (tierBadge && tierLabel) {
            tierBadge.className = `tier-pill ${data.tier_class}`;
            tierBadge.innerHTML = `<i class="fa-solid ${data.tier_icon}"></i> <span>${data.tier}</span>`;
        }

        if (tierAdviceText) tierAdviceText.textContent = data.tier_advice;
        if (recText) recText.textContent = data.tier_advice;

        // Metric Readouts
        if (valCostUsd) valCostUsd.textContent = `$${data.hourly_cost_usd.toFixed(3)}`;
        if (valCostInr) valCostInr.textContent = `(₹${data.hourly_cost_inr}/hr)`;
        if (valMonthKwh) valMonthKwh.textContent = `${data.monthly_estimate_kwh} kWh`;
        if (valMonthCost) valMonthCost.textContent = `(~$${data.monthly_cost_usd} / mo)`;
        if (valCarbon) valCarbon.textContent = `${data.carbon_kg_hr} kg`;

        // Update Charts
        initCharts(data.breakdown, data.simulated_24h);
    }

    // 7. AJAX Inference Trigger
    async function triggerPrediction() {
        if (!predictionForm) return;

        const formData = new FormData(predictionForm);
        const payload = {};
        formData.forEach((value, key) => {
            payload[key] = value;
        });

        // UI Loading State
        const btnText = btnSubmit ? btnSubmit.querySelector('.btn-content') : null;
        const btnSpinner = btnSubmit ? btnSubmit.querySelector('.btn-spinner') : null;
        if (btnText && btnSpinner) {
            btnText.style.display = 'none';
            btnSpinner.style.display = 'flex';
        }

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const json = await response.json();
            if (json.success) {
                updateAnalyticsUI(json.data);
            }
        } catch (err) {
            console.error('Inference error:', err);
        } finally {
            if (btnText && btnSpinner) {
                btnText.style.display = 'flex';
                btnSpinner.style.display = 'none';
            }
        }
    }

    // Intercept form submission for smooth AJAX
    if (predictionForm) {
        predictionForm.addEventListener('submit', (e) => {
            e.preventDefault();
            triggerPrediction();
        });
    }

    // 8. Initial Load Hydration
    if (window.INITIAL_RESULT) {
        updateAnalyticsUI(window.INITIAL_RESULT);
    } else {
        // Default initial trigger
        triggerPrediction();
    }
});
