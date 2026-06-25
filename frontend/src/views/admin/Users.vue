<template>
  <div>
    <h2>用户管理</h2>
    <div class="toolbar">
      <el-input v-model="search" placeholder="搜索昵称 / 邮箱 / 手机" clearable style="width: 260px" @keyup.enter="load" @clear="load" />
      <el-select v-model="roleFilter" placeholder="全部角色" clearable style="width: 140px" @change="load">
        <el-option label="学生" value="student" />
        <el-option label="教师" value="teacher" />
        <el-option label="管理员" value="admin" />
      </el-select>
      <el-button type="primary" @click="load">搜索</el-button>
    </div>

    <el-table :data="users" v-loading="loading" empty-text="暂无用户" style="margin-top:16px">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="nickname" label="昵称" min-width="120" />
      <el-table-column prop="email" label="邮箱" min-width="180" />
      <el-table-column prop="phone" label="手机" width="130" />
      <el-table-column label="角色" width="140">
        <template #default="{ row }">
          <el-select
            v-if="row.id !== auth.user?.id"
            :model-value="row.role"
            size="small"
            @change="(v) => changeRole(row, v)"
          >
            <el-option label="学生" value="student" />
            <el-option label="教师" value="teacher" />
            <el-option label="管理员" value="admin" />
          </el-select>
          <el-tag v-else size="small">管理员（自己）</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="points" label="积分" width="80" align="right" />
      <el-table-column label="注册时间" width="170">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../api/request'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const users = ref([])
const search = ref('')
const roleFilter = ref('')
const loading = ref(false)

const formatTime = (t) => (t ? new Date(t).toLocaleString('zh-CN') : '—')

const load = async () => {
  loading.value = true
  try {
    const params = {}
    if (search.value.trim()) params.q = search.value.trim()
    if (roleFilter.value) params.role = roleFilter.value
    users.value = (await request.get('/admin/users', { params })).data
  } finally {
    loading.value = false
  }
}

const changeRole = async (row, role) => {
  if (role === row.role) return
  try {
    await ElMessageBox.confirm(`将「${row.nickname}」的角色改为「${roleLabel(role)}」？`, '确认修改')
    await request.put(`/admin/users/${row.id}/role`, { role })
    row.role = role
    ElMessage.success('角色已更新')
  } catch (e) {
    if (e !== 'cancel' && e?.message) ElMessage.error(e.message)
  }
}

const roleLabel = (r) => ({ student: '学生', teacher: '教师', admin: '管理员' }[r] || r)

onMounted(load)
</script>

<style scoped>
.toolbar { display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
</style>
