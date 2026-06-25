<template>
  <div v-if="course">
    <div class="head">
      <div>
        <router-link to="/teacher/courses" class="back">← 返回课程列表</router-link>
        <h2>{{ course.title }}</h2>
        <el-tag>{{ course.status }}</el-tag>
      </div>
      <el-button type="primary" @click="publish" v-if="course.status === 'draft'">提交发布</el-button>
    </div>

    <div class="card form-section">
      <h3>课程信息</h3>
      <el-form :model="course" label-width="80px">
        <el-form-item label="标题"><el-input v-model="course.title" /></el-form-item>
        <el-form-item label="简介"><el-input v-model="course.description" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="价格"><el-input-number v-model="course.price" :min="0" /></el-form-item>
        <el-form-item label="划线价"><el-input-number v-model="course.original_price" :min="0" /></el-form-item>
        <el-form-item label="免费课"><el-switch v-model="course.is_free" /></el-form-item>
        <el-button type="primary" @click="saveCourse">保存课程</el-button>
      </el-form>
    </div>

    <div class="card form-section">
      <div class="head">
        <h3>课时管理</h3>
        <el-button type="primary" size="small" @click="showLesson = true">添加课时</el-button>
      </div>
      <el-table :data="lessons">
        <el-table-column prop="sort_order" label="#" width="50" />
        <el-table-column prop="title" label="标题" />
        <el-table-column label="试看" width="80">
          <template #default="{ row }">{{ row.is_free ? '是' : '否' }}</template>
        </el-table-column>
        <el-table-column prop="duration_sec" label="时长(秒)" width="100" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" type="danger" link @click="removeLesson(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="showLesson" title="添加课时" width="480px">
      <el-form :model="lessonForm" label-width="80px">
        <el-form-item label="标题"><el-input v-model="lessonForm.title" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="lessonForm.sort_order" :min="1" /></el-form-item>
        <el-form-item label="免费试看"><el-switch v-model="lessonForm.is_free" /></el-form-item>
        <el-form-item label="时长(秒)"><el-input-number v-model="lessonForm.duration_sec" :min="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showLesson = false">取消</el-button>
        <el-button type="primary" @click="addLesson">添加</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../../api/request'

const route = useRoute()
const courseId = route.params.id
const course = ref(null)
const lessons = ref([])
const showLesson = ref(false)
const lessonForm = ref({ title: '', sort_order: 1, is_free: false, duration_sec: 600 })

const load = async () => {
  const list = (await request.get('/teacher/courses')).data
  course.value = list.find((c) => String(c.id) === String(courseId))
  lessons.value = (await request.get(`/teacher/courses/${courseId}/lessons`)).data
  lessonForm.value.sort_order = lessons.value.length + 1
}

const saveCourse = async () => {
  await request.put(`/teacher/courses/${courseId}`, course.value)
  ElMessage.success('课程已保存')
}

const publish = async () => {
  await request.put(`/teacher/courses/${courseId}`, { status: 'published' })
  course.value.status = 'published'
  ElMessage.success('课程已发布，管理员可见')
}

const addLesson = async () => {
  await request.post(`/teacher/courses/${courseId}/lessons`, lessonForm.value)
  showLesson.value = false
  lessonForm.value = { title: '', sort_order: lessons.value.length + 2, is_free: false, duration_sec: 600 }
  ElMessage.success('课时已添加')
  load()
}

const removeLesson = async (id) => {
  await request.delete(`/teacher/courses/${courseId}/lessons/${id}`)
  ElMessage.success('已删除')
  load()
}

onMounted(load)
</script>

<style scoped>
.head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.back { font-size: 14px; color: var(--color-text-muted); display: block; margin-bottom: 8px; }
.form-section { padding: 24px; margin-bottom: 20px; }
.form-section h3 { margin: 0 0 16px; font-size: 16px; }
</style>
