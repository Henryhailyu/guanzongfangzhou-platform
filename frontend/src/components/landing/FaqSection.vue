<template>
  <section class="landing-section">
    <div class="landing-container">
      <div class="section-heading">
        <h2>常见问题</h2>
      </div>
      <el-collapse class="faq-list" accordion>
        <el-collapse-item v-for="(f, i) in faqs" :key="i" :title="f.q" :name="i">
          <p>{{ f.a }}</p>
        </el-collapse-item>
      </el-collapse>
    </div>
  </section>
</template>

<script setup>
import { faqs } from '../../data/landing.mock.js'
</script>

<style scoped>
.faq-list { max-width: 800px; margin: 0 auto; border: none; }
.faq-list :deep(.el-collapse-item__header) {
  background: rgba(255,255,255,0.05); color: #fff; border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px; margin-bottom: 8px; padding: 0 20px; font-size: 15px;
}
.faq-list :deep(.el-collapse-item__wrap) { background: transparent; border: none; }
.faq-list :deep(.el-collapse-item__content) {
  color: var(--landing-text-muted); padding: 16px 20px; line-height: 1.8; font-size: 14px;
}
</style>
