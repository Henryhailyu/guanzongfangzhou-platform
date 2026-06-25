<template>
  <div>
    <h2>平台数据看板</h2>
    <div class="compact-stat-grid">
      <div v-for="card in statCards" :key="card.key" class="card compact-stat-card" :class="{ highlight: card.highlight }">
        <div class="stat-title">{{ card.label }}</div>
        <div class="stat-value">{{ card.format(stats[card.key]) }}</div>
      </div>
    </div>

    <div v-if="stats.pending_teachers > 0" class="alert card">
      <span>有 {{ stats.pending_teachers }} 位教师待审核</span>
      <router-link to="/admin/teachers?status=pending" class="link">立即处理 →</router-link>
    </div>

    <div class="quick-links">
      <router-link to="/admin/analytics" class="card link-card">数据分析</router-link>
      <router-link to="/admin/questions" class="card link-card">题库管理</router-link>
      <router-link to="/admin/settings" class="card link-card">系统设置</router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../../api/request'

const stats = ref({})

const statCards = [
  { key: 'user_count', label: '用户数', format: (v) => v ?? 0 },
  { key: 'teacher_count', label: '已通过教师', format: (v) => v ?? 0 },
  { key: 'pending_teachers', label: '待审核教师', format: (v) => v ?? 0 },
  { key: 'course_count', label: '已上架课程', format: (v) => v ?? 0 },
  { key: 'order_count', label: '已支付订单', format: (v) => v ?? 0 },
  { key: 'total_revenue', label: '累计营收', highlight: true, format: (v) => `¥${Number(v || 0).toFixed(2)}` },
]

onMounted(async () => {
  stats.value = (await request.get('/admin/dashboard')).data
})
</script>

<style scoped>
.alert {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 24px;
  padding: 14px 18px;
  background: #fffbeb;
  border: 1px solid #fde68a;
}
.link { color: var(--color-primary, #4f6ef7); font-weight: 500; }
.quick-links {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
  margin-top: 24px;
}
.link-card {
  padding: 18px;
  text-align: center;
  color: var(--color-text);
  transition: box-shadow 0.2s;
}
.link-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
</style>
