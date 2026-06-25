<template>
  <section class="landing-section" id="teacher-join">
    <div class="landing-container split-layout">
      <div class="split-content">
        <div class="section-heading align-left">
          <h2>你负责教学，我们帮你完成课程交付、学员运营与商业转化。</h2>
          <p>On-Board 管综方舟为管理类联考老师提供课程发布、学员管理、题库运营、收入结算、推广链接和 AI 助教能力，让优秀老师更容易被看见、被购买、被持续复购。</p>
        </div>
        <div class="grid-2 benefit-grid">
          <div v-for="b in teacherBenefits" :key="b.title" class="benefit glass-card">
            <h3>{{ b.title }} <span v-if="b.badge" class="badge">{{ b.badge }}</span></h3>
            <p>{{ b.desc }}</p>
          </div>
        </div>
        <div class="cta-row">
          <router-link to="/register/teacher" class="landing-btn-primary">申请成为入驻老师 →</router-link>
          <a href="#teacher-join" class="landing-btn-outline">查看教师入驻权益</a>
        </div>
      </div>
      <div class="split-photo fade-in-up">
        <img src="/images/landing/scene-classroom.png" alt="管综方舟名师课堂授课场景" loading="lazy" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { teacherBenefits } from '../../data/landing.mock.js'
</script>

<style scoped>
.split-layout {
  display: grid;
  grid-template-columns: 1fr 440px;
  gap: 48px;
  align-items: center;
}
.align-left { text-align: left; margin: 0 0 28px; max-width: none; }
.align-left p { text-align: left; }
.benefit h3 { margin: 0 0 12px; font-size: 16px; }
.benefit p { margin: 0; font-size: 14px; color: var(--landing-text-muted); line-height: 1.7; }
.badge { font-size: 11px; background: rgba(212,168,83,0.2); color: #e8c468; padding: 2px 8px; border-radius: 4px; }
.cta-row { display: flex; flex-wrap: wrap; gap: 16px; margin-top: 32px; }
.split-photo {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.split-photo img {
  width: 100%;
  height: 100%;
  min-height: 520px;
  object-fit: cover;
  display: block;
}
@media (max-width: 1024px) {
  .split-layout { grid-template-columns: 1fr; }
  .split-photo { max-height: 320px; }
  .split-photo img { min-height: 280px; }
}
</style>
