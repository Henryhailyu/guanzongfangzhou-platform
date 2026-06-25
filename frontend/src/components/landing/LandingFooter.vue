<template>
  <footer class="landing-footer">
    <div class="landing-container">
      <div class="footer-top">
        <div class="brand-block">
          <div class="brand-name">On-Board 管综方舟</div>
          <div class="brand-slogan">你的管理类联考上岸驾驶舱</div>
        </div>
        <div class="footer-links">
          <a v-for="link in footerLinks" :key="link.label" :href="link.href">{{ link.label }}</a>
        </div>
      </div>
      <div class="footer-bottom">
        © 2026 On-Board 管综方舟. All rights reserved. · 备案信息占位
      </div>
    </div>
  </footer>
</template>

<script setup>
import { footerLinks } from '../../data/landing.mock.js'
</script>

<style scoped>
.landing-footer {
  background: #060d18; padding: 48px 0 32px; border-top: 1px solid rgba(255,255,255,0.08);
}
.footer-top {
  display: flex; justify-content: space-between; align-items: flex-start;
  flex-wrap: wrap; gap: 32px; margin-bottom: 32px;
}
.brand-name { font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 8px; }
.brand-slogan { font-size: 14px; color: rgba(255,255,255,0.5); }
.footer-links { display: flex; flex-wrap: wrap; gap: 20px; }
.footer-links a { color: rgba(255,255,255,0.6); text-decoration: none; font-size: 14px; }
.footer-links a:hover { color: #fff; }
.footer-bottom { font-size: 13px; color: rgba(255,255,255,0.35); text-align: center; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.06); }
</style>
