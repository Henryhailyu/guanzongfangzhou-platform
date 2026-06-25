<template>
  <div>
    <h2>教师审核</h2>
    <el-table :data="teachers" style="margin-top:16px">
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column prop="real_name" label="姓名" />
      <el-table-column prop="expertise" label="擅长" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220">
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
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../api/request'

const teachers = ref([])
const statusLabel = (s) => ({ pending: '待审核', approved: '已通过', rejected: '已拒绝', suspended: '已暂停' }[s] || s)
const statusType = (s) => ({ pending: 'warning', approved: 'success', rejected: 'info', suspended: 'danger' }[s] || '')

const load = async () => { teachers.value = (await request.get('/admin/teachers')).data }

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

onMounted(load)
</script>
