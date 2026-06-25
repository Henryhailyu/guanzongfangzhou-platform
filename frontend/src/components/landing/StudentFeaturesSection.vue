<template>
  <section class="landing-section section-light" id="features">
    <div class="landing-container">
      <div class="section-heading">
        <h2>为管理类联考设计的完整学习系统</h2>
      </div>
      <div class="split-layout reverse">
        <div class="split-photo fade-in-up">
          <img src="/images/landing/scene-study-home.png" alt="在家使用管综方舟学习的考生" loading="lazy" />
        </div>
        <div class="grid-2 feature-grid">
          <router-link v-for="f in studentFeatures" :key="f.title" :to="f.link" class="feature-card link-card fade-in-up">
            <h3>{{ f.title }}</h3>
            <p>{{ f.desc }}</p>
            <span class="more">了解更多 →</span>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { studentFeatures } from '../../data/landing.mock.js'
</script>

<style scoped>
.split-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: stretch;
}
.split-layout.reverse .split-photo { order: -1; }
.split-photo {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.1);
}
.split-photo img {
  width: 100%;
  height: 100%;
  min-height: 520px;
  object-fit: cover;
  display: block;
}
.feature-grid { align-content: start; }
.link-card { text-decoration: none; color: inherit; display: block; }
.more { display: inline-block; margin-top: 16px; font-size: 14px; color: var(--color-primary); font-weight: 500; }
@media (max-width: 1024px) {
  .split-layout { grid-template-columns: 1fr; }
  .split-layout.reverse .split-photo { order: -1; max-height: 300px; }
  .split-photo img { min-height: 260px; }
  .feature-grid { grid-template-columns: 1fr; }
}
</style>
