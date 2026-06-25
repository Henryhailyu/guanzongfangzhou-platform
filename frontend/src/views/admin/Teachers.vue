<template>
  <div>
    <h2>教师审核</h2>
    <div class="toolbar">
      <el-select v-model="statusFilter" placeholder="全部状态" clearable style="width: 140px" @change="load">
        <el-option label="待审核" value="pending" />
        <el-option label="已通过" value="approved" />
        <el-option label="已拒绝" value="rejected" />
        <el-option label="已暂停" value="suspended" />
      </el-select>
    </div>

    <el-table :data="teachers" v-loading="loading" empty-text="暂无教师" style="margin-top:16px">
      <el-table-column prop="nickname" label="昵称" width="120" />
      <el-table-column prop="real_name" label="姓名" width="100" />
      <el-table-column prop="email" label="邮箱" min-width="160" />
      <el-table-column prop="expertise" label="擅长" width="120" />
      <el-table-column label="简介" min-width="160">
        <template #default="{ row }">
          <el-popover v-if="row.bio" placement="top" :width="320" trigger="hover">
            <template #reference>
              <span class="bio-preview">{{ truncate(row.bio, 40) }}</span>
            </template>
            <p class="bio-full">{{ row.bio }}</p>
          </el-popover>
          <span v-else class="muted">—</span>
        </template>
      </el-table-column>
      <el-table-column label="分成比例" width="130">
        <template #default="{ row }">
          <template v-if="row.status === 'approved'">
            <el-input-number
              v-model="row._commission"
              :min="0"
              :max="1"
              :step="0.05"
              :precision="2"
              size="small"
              controls-position="right"
              style="width: 100px"
            />
            <el-button link type="primary" size="small" @click="saveCommission(row)">保存</el-button>
          </template>
          <span v-else>{{ (row.commission_rate * 100).toFixed(0) }}%</span>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" size="small" type="primary" @click="approve(row.user_id)">通过</el-button>
          <el-button v-if="row.status === 'pending'" size="small" @click="reject(row.user_id)">拒绝</el-button>
          <el-button v-if="row.status === 'approved'" size="small" type="danger" @click="suspend(row.user_id)">暂停</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../api/request'

const route = useRoute()
const teachers = ref([])
const statusFilter = ref(route.query.status || '')
const loading = ref(false)

const statusLabel = (s) => ({ pending: '待审核', approved: '已通过', rejected: '已拒绝', suspended: '已暂停' }[s] || s)
const statusType = (s) => ({ pending: 'warning', approved: 'success', rejected: 'info', suspended: 'danger' }[s] || '')
const truncate = (s, n) => (s.length > n ? s.slice(0, n) + '…' : s)

const load = async () => {
  loading.value = true
  try {
    const params = {}
    if (statusFilter.value) params.status = statusFilter.value
    const data = (await request.get('/admin/teachers', { params })).data
    teachers.value = data.map((t) => ({ ...t, _commission: t.commission_rate }))
  } finally {
    loading.value = false
  }
}

const approve = async (id) => {
  await request.put(`/admin/teachers/${id}/approve`)
  ElMessage.success('已通过')
  load()
}

const reject = async (id) => {
  await ElMessageBox.confirm('确定拒绝该教师的入驻申请？', '确认')
  await request.put(`/admin/teachers/${id}/reject`)
  ElMessage.success('已拒绝')
  load()
}

const suspend = async (id) => {
  await request.put(`/admin/teachers/${id}/suspend`)
  ElMessage.success('已暂停')
  load()
}

const saveCommission = async (row) => {
  try {
    await request.put(`/admin/teachers/${row.user_id}/commission`, { commission_rate: row._commission })
    row.commission_rate = row._commission
    ElMessage.success('分成比例已更新')
  } catch (e) {
    ElMessage.error(e.message)
  }
}

watch(() => route.query.status, (v) => {
  statusFilter.value = v || ''
  load()
})

onMounted(load)
</script>

<style scoped>
.toolbar { margin-top: 16px; }
.bio-preview { cursor: help; color: var(--color-text-secondary, #6b7280); }
.bio-full { margin: 0; line-height: 1.6; white-space: pre-wrap; }
.muted { color: #9ca3af; }
</style>
