<template>
  <div>
    <h2>教师工作台</h2>

    <div v-if="status === 'pending'" class="pending-panel card">
      <div class="icon">⏳</div>
      <h3>入驻申请审核中</h3>
      <p>我们已收到你的入驻申请，管理员通常在 1–3 个工作日内完成审核。审核通过后即可创建课程、管理学员与查看收入。</p>
      <ul>
        <li>姓名：{{ profile.real_name || '—' }}</li>
        <li>擅长科目：{{ expertiseLabel }}</li>
      </ul>
    </div>

    <div v-else-if="status === 'rejected'" class="pending-panel card">
      <div class="icon">✕</div>
      <h3>入驻申请未通过</h3>
      <p>如有疑问，请联系平台管理员了解详情。</p>
    </div>

    <div v-else-if="status === 'suspended'" class="pending-panel card">
      <div class="icon">⚠</div>
      <h3>账号已暂停</h3>
      <p>你的教师账号已被暂停，请联系平台管理员。</p>
    </div>

    <div v-else class="compact-stat-grid">
      <div class="card compact-stat-card">
        <div class="stat-title">课程数</div>
        <div class="stat-value">{{ stats.course_count }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">学员数</div>
        <div class="stat-value">{{ stats.student_count }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">总收入</div>
        <div class="stat-value">¥{{ stats.total_revenue }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">分成比例</div>
        <div class="stat-value">{{ (stats.commission_rate * 100).toFixed(0) }}%</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '../../stores/auth'
import request from '../../api/request'

const auth = useAuthStore()
const stats = ref({ course_count: 0, student_count: 0, total_revenue: 0, commission_rate: 0.7 })
const profile = ref({})

const status = computed(() => auth.teacherStatus)
const expertiseLabel = computed(() => {
  const map = { math: '数学基础', logic: '逻辑推理', writing: '写作', english: '英语二', combo: '综合' }
  return map[profile.value.expertise] || profile.value.expertise || '—'
})

onMounted(async () => {
  await auth.fetchMe()
  try {
    profile.value = (await request.get('/teacher/profile')).data
  } catch { /* pending */ }

  if (auth.isApprovedTeacher) {
    stats.value = (await request.get('/teacher/dashboard')).data
  }
})
</script>

<style scoped>
.pending-panel { margin-top: 24px; padding: 32px; text-align: center; max-width: 560px; }
.pending-panel .icon { font-size: 48px; margin-bottom: 16px; }
.pending-panel h3 { margin: 0 0 12px; }
.pending-panel p { color: var(--color-text-muted); line-height: 1.7; margin: 0 0 20px; }
.pending-panel ul { text-align: left; display: inline-block; color: var(--color-text-muted); line-height: 1.8; }
</style>
