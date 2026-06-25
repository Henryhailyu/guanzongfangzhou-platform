<template>
  <section class="solution-section landing-section" id="solution">
    <AnimatedBlueBg />
    <div class="landing-container solution-inner">
      <div class="section-heading fade-in-up">
        <h2>把漫长备考，拆成每天能完成的上岸航线。</h2>
      </div>
      <div class="steps">
        <div
          v-for="(s, i) in solutionSteps"
          :key="s.step"
          class="step step-card fade-in-up"
          :style="{ animationDelay: `${0.1 + i * 0.12}s` }"
        >
          <div class="step-badge">{{ s.step }}</div>
          <h3>{{ s.title }}</h3>
          <p>{{ s.desc }}</p>
          <div v-if="i < solutionSteps.length - 1" class="arrow">→</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { solutionSteps } from '../../data/landing.mock.js'
import AnimatedBlueBg from './AnimatedBlueBg.vue'
</script>

<style scoped>
.solution-section {
  position: relative;
  overflow: hidden;
  background: #1e4080;
}

.solution-inner {
  position: relative;
  z-index: 1;
}

.steps {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: center;
}

.step-card {
  flex: 1;
  min-width: 180px;
  max-width: 220px;
  position: relative;
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 16px;
  padding: 24px 20px;
  transition: transform 0.3s, box-shadow 0.3s, background 0.3s;
}

.step-card:hover {
  transform: translateY(-6px);
  background: rgba(255, 255, 255, 0.14);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.15);
}

.step-badge {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #22d3ee, #4f6ef7);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  box-shadow: 0 4px 16px rgba(34, 211, 238, 0.35);
}

.step-card h3 {
  margin: 0 0 8px;
  font-size: 16px;
  color: #fff;
}

.step-card p {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.78);
  line-height: 1.6;
}

.arrow {
  display: none;
}

@media (min-width: 1024px) {
  .step-card .arrow {
    display: block;
    position: absolute;
    right: -20px;
    top: 28px;
    color: rgba(255, 255, 255, 0.45);
    font-size: 20px;
  }
  .step-card:last-child .arrow {
    display: none;
  }
}

@media (max-width: 768px) {
  .steps {
    flex-direction: column;
    align-items: center;
  }
  .step-card {
    max-width: 100%;
    width: 100%;
  }
}
</style>
