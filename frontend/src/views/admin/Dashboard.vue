<template>
  <div>
    <h2>平台数据看板</h2>
    <div class="compact-stat-grid">
      <div v-for="(label, key) in labels" :key="key" class="card compact-stat-card">
        <div class="stat-title">{{ label }}</div>
        <div class="stat-value">{{ stats[key] ?? 0 }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../../api/request'

const stats = ref({})
const labels = {
  user_count: '用户数',
  teacher_count: '教师数',
  pending_teachers: '待审核',
  course_count: '课程数',
  order_count: '订单数',
}

onMounted(async () => {
  stats.value = (await request.get('/admin/dashboard')).data
})
</script>
