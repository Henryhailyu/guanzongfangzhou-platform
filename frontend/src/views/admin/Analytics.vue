<template>
  <div>
    <h2>数据分析</h2>
    <p class="desc">近 7 日平台运营概况</p>

    <div class="compact-stat-grid">
      <div class="card compact-stat-card highlight">
        <div class="stat-title">7 日营收</div>
        <div class="stat-value">¥{{ Number(data.revenue_7d || 0).toFixed(2) }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">新增用户</div>
        <div class="stat-value">{{ data.new_users_7d ?? 0 }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">成交订单</div>
        <div class="stat-value">{{ data.orders_7d ?? 0 }}</div>
      </div>
    </div>

    <div class="grid-2">
      <section class="card panel">
        <h3>题库分布</h3>
        <el-table :data="data.question_stats || []" size="small">
          <el-table-column prop="subject_label" label="科目" />
          <el-table-column prop="count" label="题目数" align="right" />
        </el-table>
      </section>

      <section class="card panel">
        <h3>最近成交订单</h3>
        <el-table :data="data.recent_orders || []" size="small" empty-text="暂无订单">
          <el-table-column prop="user_nickname" label="用户" width="90" />
          <el-table-column prop="product_title" label="商品" min-width="120" show-overflow-tooltip />
          <el-table-column label="金额" width="80" align="right">
            <template #default="{ row }">¥{{ row.amount }}</template>
          </el-table-column>
          <el-table-column label="时间" width="150">
            <template #default="{ row }">{{ formatTime(row.paid_at || row.created_at) }}</template>
          </el-table-column>
        </el-table>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../../api/request'

const data = ref({})

const formatTime = (t) => (t ? new Date(t).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) : '—')

onMounted(async () => {
  data.value = (await request.get('/admin/analytics')).data
})
</script>

<style scoped>
.desc { color: var(--color-text-secondary, #6b7280); margin: 8px 0 20px; }
.grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 24px;
}
.panel { padding: 20px; }
.panel h3 { margin: 0 0 14px; font-size: 15px; }
</style>
