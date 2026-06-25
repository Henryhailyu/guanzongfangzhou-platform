<template>
  <div>
    <h2>课程管理</h2>
    <el-table :data="courses" style="margin-top:16px">
      <el-table-column prop="title" label="课程" min-width="180" />
      <el-table-column prop="teacher_name" label="教师" width="120" />
      <el-table-column prop="price" label="价格" width="80" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column prop="lesson_count" label="课时" width="80" />
      <el-table-column prop="student_count" label="学员" width="80" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button v-if="row.status !== 'published'" size="small" type="primary" @click="setStatus(row.id, 'published')">上架</el-button>
          <el-button v-if="row.status === 'published'" size="small" @click="setStatus(row.id, 'archived')">下架</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../api/request'

const courses = ref([])
const load = async () => { courses.value = (await request.get('/admin/courses')).data }

const setStatus = async (id, status) => {
  await request.put(`/admin/courses/${id}/status`, { status })
  ElMessage.success(status === 'published' ? '已上架' : '已下架')
  load()
}

onMounted(load)
</script>
