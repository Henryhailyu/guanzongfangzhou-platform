<template>
  <section class="landing-section section-light" id="ai">
    <div class="landing-container ai-grid">
      <div class="ai-content">
        <div class="section-heading" style="text-align:left;margin:0 0 32px">
          <h2>AI 不是噱头，而是你的全天候备考助教。</h2>
          <p>管综方舟将 AI 融入做题、批改、答疑、诊断和学习计划，让每一次学习都有反馈。</p>
        </div>
        <div class="ai-list">
          <div v-for="f in aiFeatures" :key="f.title" class="ai-item">
            <div class="ai-dot"></div>
            <div>
              <strong>{{ f.title }} <span v-if="f.badge" class="badge">{{ f.badge }}</span></strong>
              <p>{{ f.desc }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="ai-visual glass-card">
        <div class="robot">🤖</div>
        <div class="chart-mock">
          <div class="bar" v-for="(h, i) in [40,65,55,80,70]" :key="i" :style="{ height: h + '%' }"></div>
        </div>
        <p class="visual-caption">AI 学习诊断 · 能力画像预览</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { aiFeatures } from '../../data/landing.mock.js'
</script>

<style scoped>
.ai-grid { display: grid; grid-template-columns: 1fr 360px; gap: 48px; align-items: center; }
.ai-item { display: flex; gap: 16px; margin-bottom: 20px; }
.ai-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--color-primary); margin-top: 8px; flex-shrink: 0; }
.ai-item strong { font-size: 16px; color: #1a1a2e; }
.ai-item p { margin: 4px 0 0; font-size: 14px; color: #6b7280; }
.badge { font-size: 11px; background: #fef3c7; color: #d97706; padding: 2px 8px; border-radius: 4px; margin-left: 8px; }
.ai-visual { text-align: center; padding: 32px; background: linear-gradient(135deg, #eef1fe, #fff) !important; border: 1px solid #e8eaed !important; }
.robot { font-size: 64px; margin-bottom: 20px; }
.chart-mock { display: flex; align-items: flex-end; justify-content: center; gap: 8px; height: 100px; margin-bottom: 12px; }
.bar { width: 24px; background: linear-gradient(180deg, #4F6EF7, #22d3ee); border-radius: 4px 4px 0 0; }
.visual-caption { font-size: 13px; color: #6b7280; margin: 0; }
@media (max-width: 768px) { .ai-grid { grid-template-columns: 1fr; } }
</style>
