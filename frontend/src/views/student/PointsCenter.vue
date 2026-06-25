<template>
  <div class="points-page">
    <h2>积分中心</h2>

    <div class="compact-stat-grid">
      <div class="card compact-stat-card highlight">
        <div class="stat-title">积分余额</div>
        <div class="stat-value">{{ overview.points }}</div>
        <div class="level-tag">{{ overview.level || '入门生' }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">今日免费额度</div>
        <div v-if="overview.quota?.unlimited" class="stat-value">无限 VIP</div>
        <template v-else>
          <div class="stat-value">{{ overview.quota?.remaining_free ?? 0 }}</div>
          <div class="stat-sub">已刷 {{ overview.quota?.free_done || 0 }} / {{ overview.quota?.free_limit || 20 }}</div>
        </template>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">今日错题</div>
        <div class="stat-value">{{ overview.quota?.wrong_count || 0 }}</div>
        <div class="stat-sub">错满 5 道提前用尽额度</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">每日签到</div>
        <el-button
          type="primary"
          size="small"
          :disabled="overview.checked_in_today"
          :loading="checkingIn"
          style="margin-top:8px"
          @click="checkin"
        >
          {{ overview.checked_in_today ? '今日已签到' : '签到 +10' }}
        </el-button>
      </div>
    </div>

    <el-alert
      v-if="overview.quota?.quota_used && !overview.quota?.unlimited"
      type="warning"
      :closable="false"
      show-icon
      class="quota-alert"
      title="今日免费刷题额度已用尽"
      description="继续刷题将每题消耗 5 积分。积分不足时请明日再来或购买积分包（即将上线）。"
    />

    <div class="rules-section">
      <h3>积分规则</h3>
      <div class="rules-grid">
        <div class="card rules-card">
          <h4>获得积分</h4>
          <ul>
            <li v-for="r in rules.earn" :key="r.key" :class="{ disabled: !r.enabled }">
              <span>{{ r.label }}</span>
              <strong>+{{ r.points }}</strong>
              <el-tag v-if="!r.enabled" size="small" type="info">即将上线</el-tag>
            </li>
          </ul>
        </div>
        <div class="card rules-card">
          <h4>消耗积分</h4>
          <ul>
            <li v-for="r in rules.spend" :key="r.key" :class="{ disabled: !r.enabled }">
              <span>{{ r.label }}</span>
              <strong>-{{ r.points }}</strong>
              <el-tag v-if="!r.enabled" size="small" type="info">即将上线</el-tag>
            </li>
          </ul>
        </div>
      </div>
      <p v-if="rules.quota" class="quota-note">{{ rules.quota.description }}</p>
    </div>

    <div class="history-section">
      <h3>积分流水</h3>
      <el-table :data="transactions" empty-text="暂无流水记录" style="width:100%">
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
        </el-table-column>
        <el-table-column prop="type_label" label="类型" width="120" />
        <el-table-column prop="description" label="说明" min-width="160" />
        <el-table-column label="变动" width="100" align="right">
          <template #default="{ row }">
            <span :class="row.amount > 0 ? 'plus' : 'minus'">
              {{ row.amount > 0 ? '+' : '' }}{{ row.amount }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="balance" label="余额" width="80" align="right" />
      </el-table>
      <el-pagination
        v-if="total > pageSize"
        class="pager"
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        v-model:current-page="page"
        @current-change="loadTransactions"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../api/request'

const overview = ref({ points: 0, level: '', quota: {}, checked_in_today: false })
const rules = ref({ earn: [], spend: [], quota: null })
const transactions = ref([])
const page = ref(1)
const pageSize = 20
const total = ref(0)
const checkingIn = ref(false)

const formatTime = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

const loadOverview = async () => {
  overview.value = (await request.get('/points/overview')).data
}

const loadRules = async () => {
  rules.value = (await request.get('/points/rules')).data
}

const loadTransactions = async () => {
  const res = await request.get('/points/transactions', { params: { page: page.value, page_size: pageSize } })
  transactions.value = res.data
  total.value = res.pagination?.total || 0
}

const checkin = async () => {
  checkingIn.value = true
  try {
    const res = await request.post('/points/checkin')
    overview.value.points = res.data.points
    overview.value.checked_in_today = true
    ElMessage.success('签到成功 +10 积分')
    loadTransactions()
  } catch (e) {
    ElMessage.warning(e.message)
  } finally {
    checkingIn.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadOverview(), loadRules(), loadTransactions()])
})
</script>

<style scoped>
.highlight { border-color: var(--color-primary); background: linear-gradient(135deg, #fff 0%, var(--color-primary-light) 100%); }
.level-tag { font-size: 12px; color: var(--color-primary); margin-top: 8px; }
.stat-sub { font-size: 12px; color: var(--color-text-muted); margin-top: 6px; }
.quota-alert { margin-top: 20px; }
.rules-section, .history-section { margin-top: 32px; }
.rules-section h3, .history-section h3 { font-size: 18px; margin: 0 0 16px; }
.rules-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.rules-card { padding: 20px; }
.rules-card h4 { margin: 0 0 12px; font-size: 15px; }
.rules-card ul { list-style: none; margin: 0; padding: 0; }
.rules-card li {
  display: flex; align-items: center; gap: 8px; justify-content: space-between;
  padding: 8px 0; border-bottom: 1px solid var(--color-border); font-size: 14px;
}
.rules-card li:last-child { border-bottom: none; }
.rules-card li.disabled { opacity: 0.55; }
.rules-card li strong { color: var(--color-primary); flex-shrink: 0; }
.quota-note { font-size: 13px; color: var(--color-text-muted); margin-top: 12px; }
.plus { color: var(--color-success); font-weight: 600; }
.minus { color: var(--color-error); font-weight: 600; }
.pager { margin-top: 16px; justify-content: flex-end; }
@media (max-width: 768px) { .rules-grid { grid-template-columns: 1fr; } }
</style>
