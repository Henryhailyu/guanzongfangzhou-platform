<template>
  <section class="landing-section section-light audience-section">
    <div class="landing-container">
      <div class="section-heading">
        <h2>无论你从哪里开始，都可以找到适合自己的上岸路径。</h2>
      </div>
      <div class="split-layout">
        <div class="grid-2 audience-grid">
          <div v-for="a in audiences" :key="a.title" class="audience feature-card">
            <div class="emoji">{{ a.emoji }}</div>
            <h3>{{ a.title }}</h3>
            <p>{{ a.desc }}</p>
          </div>
        </div>
        <div class="split-photo fade-in-up">
          <img src="/images/landing/scene-group-study.png" alt="管综备考小组学习场景" loading="lazy" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { audiences } from '../../data/landing.mock.js'
</script>

<style scoped>
.split-layout {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 40px;
  align-items: center;
}
.audience { text-align: center; }
.emoji { font-size: 36px; margin-bottom: 12px; }
.audience h3 { margin: 0 0 8px; font-size: 16px; }
.audience p { margin: 0; font-size: 14px; color: #6b7280; line-height: 1.6; }
.split-photo {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.1);
}
.split-photo img {
  width: 100%;
  height: 100%;
  min-height: 400px;
  object-fit: cover;
  display: block;
}
@media (max-width: 1024px) {
  .split-layout { grid-template-columns: 1fr; }
  .split-photo { order: -1; max-height: 280px; }
  .split-photo img { min-height: 240px; }
  .audience-grid { grid-template-columns: 1fr; }
}
</style>
