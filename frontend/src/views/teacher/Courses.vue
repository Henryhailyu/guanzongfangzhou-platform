<template>
  <div>
    <div class="head">
      <h2>我的课程</h2>
      <el-button type="primary" @click="showDialog = true">新建课程</el-button>
    </div>
    <el-table :data="courses" style="margin-top:16px">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="price" label="价格" width="100" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column prop="total_lessons" label="课时" width="80" />
      <el-table-column prop="student_count" label="学员" width="80" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <router-link :to="`/teacher/courses/${row.id}`">
            <el-button size="small" type="primary" link>管理</el-button>
          </router-link>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="showDialog" title="新建课程" width="480px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="科目">
          <el-select v-model="form.subject" style="width:100%">
            <el-option label="数学" value="math" />
            <el-option label="逻辑" value="logic" />
            <el-option label="写作" value="writing" />
            <el-option label="英语" value="english" />
          </el-select>
        </el-form-item>
        <el-form-item label="简介"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item label="价格"><el-input-number v-model="form.price" :min="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="create">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../../api/request'

const router = useRouter()
const courses = ref([])
const showDialog = ref(false)
const form = ref({ title: '', subject: 'math', description: '', price: 99 })

const load = async () => { courses.value = (await request.get('/teacher/courses')).data }

const create = async () => {
  const res = await request.post('/teacher/courses', { ...form.value, status: 'draft' })
  ElMessage.success('已创建，请添加课时后发布')
  showDialog.value = false
  router.push(`/teacher/courses/${res.data.id}`)
}

onMounted(load)
</script>

<style scoped>
.head { display: flex; justify-content: space-between; align-items: center; }
</style>
