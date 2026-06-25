<template>
  <section class="landing-section" id="courses">
    <div class="landing-container">
      <div class="section-heading">
        <h2>覆盖管理类联考全科备考场景</h2>
      </div>
      <div class="grid-4">
        <div v-for="s in examSubjects" :key="s.key" class="subject-card" :style="{ '--accent': s.color }">
          <div class="subject-icon">{{ s.name[0] }}</div>
          <h3>{{ s.name }}</h3>
          <p>{{ s.desc }}</p>
          <div class="score">{{ s.score }} 分</div>
        </div>
      </div>
      <div class="total-score">总分 300 分</div>
    </div>
  </section>
</template>

<script setup>
import { examSubjects } from '../../data/landing.mock.js'
</script>

<style scoped>
.subject-card {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px; padding: 24px; transition: transform 0.25s;
  border-top: 3px solid var(--accent);
}
.subject-card:hover { transform: translateY(-4px); }
.subject-icon {
  width: 44px; height: 44px; border-radius: 12px; background: var(--accent);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 18px; margin-bottom: 16px; color: #fff;
}
.subject-card h3 { margin: 0 0 12px; font-size: 18px; }
.subject-card p { margin: 0; font-size: 14px; color: var(--landing-text-muted); line-height: 1.6; }
.score { margin-top: 16px; font-size: 14px; color: var(--accent); font-weight: 600; }
.total-score { text-align: center; margin-top: 32px; font-size: 18px; color: var(--landing-accent-gold); font-weight: 600; }
</style>
