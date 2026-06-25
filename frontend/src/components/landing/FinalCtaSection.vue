<template>
  <section class="final-cta">
    <div class="cta-bg" :style="{ backgroundImage: `url(${ctaBg})` }"></div>
    <div class="cta-overlay"></div>
    <div class="landing-container cta-content">
      <h2>现在登上管综方舟，向上岸出发。</h2>
      <p>无论你是正在备考的考生，还是希望扩大课程影响力的管理类联考老师，On-Board 管综方舟都为你准备好了完整路径。</p>
      <div class="cta-buttons">
        <router-link to="/register/student" class="landing-btn-primary">我是考生，开始备考 →</router-link>
        <router-link to="/register/teacher" class="landing-btn-outline">我是老师，申请入驻 →</router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
const ctaBg = '/images/landing/final-cta-bg.png'
</script>

<style scoped>
.final-cta {
  position: relative; padding: 100px 0; overflow: hidden; text-align: center;
}
.cta-bg { position: absolute; inset: 0; background-size: cover; background-position: center 40%; }
.cta-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(15, 35, 70, 0.78) 0%, rgba(15, 35, 70, 0.85) 50%, rgba(15, 35, 70, 0.9) 100%);
}
.cta-content { position: relative; z-index: 1; max-width: 720px; }
h2 { font-size: clamp(28px, 4vw, 40px); margin: 0 0 16px; font-weight: 700; }
p { font-size: 17px; color: rgba(255,255,255,0.8); line-height: 1.8; margin: 0 0 32px; }
.cta-buttons { display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; }
@media (max-width: 768px) {
  .cta-buttons { flex-direction: column; align-items: center; }
  .cta-buttons a { width: 100%; max-width: 320px; justify-content: center; }
}
</style>
