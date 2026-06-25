<template>
  <div>
    <h2>题库管理</h2>
    <div class="toolbar">
      <el-select v-model="subject" placeholder="全部科目" clearable style="width: 140px" @change="onFilterChange">
        <el-option label="数学" value="math" />
        <el-option label="逻辑" value="logic" />
        <el-option label="写作" value="writing" />
        <el-option label="英语二" value="english" />
      </el-select>
      <span class="total-hint">共 {{ total }} 题</span>
    </div>

    <el-table :data="questions" v-loading="loading" empty-text="暂无题目" style="margin-top:16px">
      <el-table-column prop="question_id" label="题号" width="100" />
      <el-table-column prop="subject_label" label="科目" width="90" />
      <el-table-column prop="question_type" label="题型" width="100" />
      <el-table-column prop="difficulty" label="难度" width="80" />
      <el-table-column prop="tag" label="标签" width="120" />
      <el-table-column label="题干" min-width="240">
        <template #default="{ row }">
          <el-popover v-if="row.stem" placement="top" :width="400" trigger="hover">
            <template #reference>
              <span class="stem-preview">{{ truncate(row.stem, 60) }}</span>
            </template>
            <p class="stem-full">{{ row.stem }}</p>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="correct_answer" label="答案" width="80" />
      <el-table-column label="作答统计" width="120">
        <template #default="{ row }">
          <span v-if="row.stats?.total_attempts">{{ row.stats.total_attempts }} 次 / {{ row.stats.correct_rate != null ? (row.stats.correct_rate * 100).toFixed(0) + '%' : '—' }}</span>
          <span v-else class="muted">—</span>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > pageSize"
      class="pager"
      layout="total, prev, pager, next"
      :total="total"
      :page-size="pageSize"
      v-model:current-page="page"
      @current-change="load"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../../api/request'

const questions = ref([])
const subject = ref('')
const page = ref(1)
const pageSize = 20
const total = ref(0)
const loading = ref(false)

const truncate = (s, n) => (s && s.length > n ? s.slice(0, n) + '…' : s || '')

const load = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize }
    if (subject.value) params.subject = subject.value
    const res = await request.get('/admin/questions', { params })
    questions.value = res.data
    total.value = res.pagination?.total || 0
  } finally {
    loading.value = false
  }
}

const onFilterChange = () => {
  page.value = 1
  load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { display: flex; align-items: center; gap: 16px; margin-top: 16px; }
.total-hint { color: var(--color-text-secondary, #6b7280); font-size: 14px; }
.stem-preview { cursor: help; }
.stem-full { margin: 0; line-height: 1.6; white-space: pre-wrap; }
.muted { color: #9ca3af; }
.pager { margin-top: 20px; justify-content: flex-end; }
</style>
