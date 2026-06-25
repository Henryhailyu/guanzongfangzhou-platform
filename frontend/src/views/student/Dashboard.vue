<template>
  <div>
    <h2>学习中心</h2>
    <div class="compact-stat-grid">
      <router-link to="/points" class="stat-link">
        <div class="card compact-stat-card highlight">
          <div class="stat-title">积分余额</div>
          <div class="stat-value">{{ points }}</div>
          <div class="stat-sub">点击查看积分中心 →</div>
        </div>
      </router-link>
      <div class="card compact-stat-card">
        <div class="stat-title">今日已刷</div>
        <div class="stat-value">{{ quota.free_done || 0 }}</div>
        <div v-if="!quota.unlimited" class="stat-sub">剩余免费 {{ quota.remaining_free ?? remainingFree }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">累计答题</div>
        <div class="stat-value">{{ progress.summary?.total_answered || 0 }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">总正确率</div>
        <div class="stat-value">{{ progress.summary?.accuracy || 0 }}%</div>
      </div>
    </div>

    <h3 class="section-title">各科目进度</h3>
    <div v-if="progress.subjects?.length" class="compact-stat-grid">
      <div v-for="s in progress.subjects" :key="s.subject" class="card compact-stat-card">
        <div class="stat-title">{{ s.label }}</div>
        <div class="stat-row"><span>已答</span><strong>{{ s.total_answered }}</strong></div>
        <div class="stat-row"><span>正确率</span><strong>{{ s.accuracy }}%</strong></div>
        <div class="stat-row"><span>错题</span><strong>{{ s.wrong_count }}</strong></div>
        <el-progress :percentage="s.accuracy" :stroke-width="6" style="margin-top:12px" />
      </div>
    </div>
    <el-empty v-else description="还没有答题记录，去刷题吧！" />

    <div class="actions">
      <el-button type="primary" @click="$router.push('/practice')">去刷题</el-button>
      <el-button @click="$router.push('/points')">积分中心</el-button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import request from '../../api/request'

const points = ref(0)
const quota = ref({})
const progress = ref({ subjects: [], summary: {} })

const remainingFree = computed(() => {
  if (quota.value.unlimited) return '∞'
  const limit = quota.value.free_limit || 20
  const done = quota.value.free_done || 0
  return quota.value.quota_used ? 0 : Math.max(0, limit - done)
})

onMounted(async () => {
  const [b, q, p] = await Promise.all([
    request.get('/points/balance'),
    request.get('/points/quota/today'),
    request.get('/learning/progress'),
  ])
  points.value = b.data.points
  quota.value = q.data
  progress.value = p.data
})
</script>

<style scoped>
.section-title { margin: 32px 0 0; font-size: 18px; }
.actions { margin-top: 32px; display: flex; gap: 12px; }
.stat-link { text-decoration: none; color: inherit; }
.highlight { border-color: var(--color-primary); }
.stat-sub { font-size: 12px; color: var(--color-text-muted); margin-top: 6px; }
</style>
