<template>
  <section class="landing-section section-light">
    <div class="landing-container split-layout">
      <div class="split-content">
        <div class="section-heading align-left">
          <h2>你不是不努力，而是备考系统不够清晰。</h2>
          <p>管理类联考的难点，不只是知识点多，而是时间紧、题型杂、反馈慢、复盘弱。管综方舟把备考过程拆成可执行、可追踪、可反馈的每日路径。</p>
        </div>
        <div class="grid-2 pain-grid">
          <div v-for="(p, i) in painPoints" :key="i" class="feature-card fade-in-up" :style="{ animationDelay: `${i * 0.08}s` }">
            <div class="num">{{ i + 1 }}</div>
            <h3>{{ p.title }}</h3>
            <p>{{ p.desc }}</p>
          </div>
        </div>
      </div>
      <div class="split-photo fade-in-up">
        <img src="/images/landing/scene-study-focus.png" alt="专注备考的管综考生" loading="lazy" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { painPoints } from '../../data/landing.mock.js'
</script>

<style scoped>
.split-layout {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 48px;
  align-items: center;
}
.align-left { text-align: left; margin: 0 0 32px; max-width: none; }
.pain-grid { margin-top: 0; }
.num {
  width: 32px; height: 32px; border-radius: 8px; background: var(--color-primary-light);
  color: var(--color-primary); font-weight: 700; display: flex; align-items: center; justify-content: center;
  font-size: 14px; margin-bottom: 16px;
}
.split-photo {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.1);
}
.split-photo img {
  width: 100%;
  height: 100%;
  min-height: 480px;
  object-fit: cover;
  display: block;
}
@media (max-width: 1024px) {
  .split-layout { grid-template-columns: 1fr; }
  .split-photo { order: -1; max-height: 320px; }
  .split-photo img { min-height: 280px; }
}
</style>
