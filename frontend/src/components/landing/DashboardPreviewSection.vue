<template>
  <section class="landing-section">
    <div class="landing-container">
      <div class="section-heading">
        <h2>你的备考进度，不再靠感觉判断。</h2>
        <p>管综方舟不只记录你学了多久，更关注你哪里变强了、哪里还需要突破。</p>
      </div>
      <div class="dashboard-grid">
        <div v-for="m in dashboardMetrics" :key="m.label" class="metric glass-card">
          <div class="metric-icon">{{ m.icon }}</div>
          <div class="metric-value">{{ m.value }}</div>
          <div class="metric-label">{{ m.label }}</div>
          <div v-if="m.trend" class="metric-trend">{{ m.trend }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { dashboardMetrics } from '../../data/landing.mock.js'
</script>

<style scoped>
.dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; }
.metric { text-align: center; padding: 20px 16px; }
.metric-icon { font-size: 24px; margin-bottom: 8px; }
.metric-value { font-size: 24px; font-weight: 700; color: #22d3ee; margin-bottom: 4px; }
.metric-label { font-size: 13px; color: var(--landing-text-muted); }
.metric-trend { font-size: 11px; color: #10b981; margin-top: 6px; }
@media (max-width: 1024px) { .dashboard-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .dashboard-grid { grid-template-columns: 1fr; } }
</style>
