<template>
  <div class="animated-blue-bg" aria-hidden="true">
    <div class="bg-base"></div>
    <div class="bg-mesh"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
    <div class="particles">
      <span v-for="n in 18" :key="n" class="dot" :style="dotStyle(n)"></span>
    </div>
  </div>
</template>

<script setup>
const dotStyle = (n) => {
  const left = ((n * 17 + 7) % 100)
  const top = ((n * 23 + 11) % 100)
  const delay = (n * 0.35) % 5
  const duration = 4 + (n % 4)
  return {
    left: `${left}%`,
    top: `${top}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
  }
}
</script>

<style scoped>
.animated-blue-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.bg-base {
  position: absolute;
  inset: 0;
  background: linear-gradient(145deg, #1a4d8f 0%, #2563b8 42%, #1e4080 100%);
}

.bg-mesh {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 20% 30%, rgba(34, 211, 238, 0.18) 0%, transparent 55%),
    radial-gradient(ellipse 70% 50% at 80% 70%, rgba(139, 92, 246, 0.14) 0%, transparent 55%);
  animation: meshShift 12s ease-in-out infinite alternate;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.55;
}

.orb-1 {
  width: 320px;
  height: 320px;
  background: #22d3ee;
  top: -80px;
  left: -60px;
  animation: floatOrb1 14s ease-in-out infinite;
}

.orb-2 {
  width: 280px;
  height: 280px;
  background: #8b5cf6;
  bottom: -60px;
  right: 10%;
  animation: floatOrb2 16s ease-in-out infinite;
}

.orb-3 {
  width: 200px;
  height: 200px;
  background: #60a5fa;
  top: 40%;
  right: -40px;
  animation: floatOrb3 11s ease-in-out infinite;
}

.orb-4 {
  width: 160px;
  height: 160px;
  background: #38bdf8;
  bottom: 20%;
  left: 25%;
  animation: floatOrb4 13s ease-in-out infinite;
}

.particles {
  position: absolute;
  inset: 0;
}

.dot {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.35);
  animation: twinkle ease-in-out infinite;
}

@keyframes meshShift {
  from { opacity: 0.85; transform: scale(1); }
  to { opacity: 1; transform: scale(1.04); }
}

@keyframes floatOrb1 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(40px, 30px); }
}

@keyframes floatOrb2 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-35px, -25px); }
}

@keyframes floatOrb3 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-20px, 35px); }
}

@keyframes floatOrb4 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(25px, -20px); }
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.4); }
}

@media (prefers-reduced-motion: reduce) {
  .bg-mesh, .orb, .dot { animation: none; }
}
</style>
