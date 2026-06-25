<template>
  <div>
    <h2>我的学员</h2>
    <el-table :data="students" style="margin-top:16px">
      <el-table-column prop="nickname" label="学员" />
      <el-table-column prop="course_title" label="课程" />
      <el-table-column prop="progress_pct" label="进度%" width="100" />
      <el-table-column prop="enrolled_at" label="报名时间" />
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../../api/request'
const students = ref([])
onMounted(async () => { students.value = (await request.get('/teacher/students')).data })
</script>
