<template>
  <div>
    <h2>课程中心</h2>
    <el-tabs v-model="tab" @tab-change="load">
      <el-tab-pane label="全部课程" name="all" />
      <el-tab-pane label="我的课程" name="mine" />
    </el-tabs>

    <div v-if="tab === 'all'" class="compact-stat-grid">
      <div
        v-for="c in courses"
        :key="c.id"
        class="card compact-stat-card course-card"
        @click="$router.push(`/courses/${c.id}`)"
      >
        <div class="stat-title">{{ c.title }}</div>
        <div class="subject">{{ subjectLabel(c.subject) }} · {{ c.teacher_name }}</div>
        <div class="price-row">
          <span v-if="c.original_price" class="orig">¥{{ c.original_price }}</span>
          <span class="now">{{ c.is_free || c.price === 0 ? '免费' : `¥${c.price}` }}</span>
        </div>
        <div class="stat-sub">{{ c.student_count }} 人学习 · {{ c.total_lessons }} 课时</div>
      </div>
    </div>

    <div v-else-if="!auth.isLoggedIn" class="login-prompt card">
      <p>登录后查看已购课程</p>
      <router-link to="/login"><el-button type="primary">去登录</el-button></router-link>
    </div>
    <div v-else class="compact-stat-grid">
      <div
        v-for="c in enrolled"
        :key="c.id"
        class="card compact-stat-card course-card"
        @click="goLearn(c)"
      >
        <div class="stat-title">{{ c.title }}</div>
        <div class="stat-sub">进度 {{ c.progress_pct || 0 }}%</div>
        <el-progress :percentage="c.progress_pct || 0" :stroke-width="6" style="margin-top:12px" />
        <el-button type="primary" link style="margin-top:8px">继续学习 →</el-button>
      </div>
      <el-empty v-if="!enrolled.length" description="还没有购买课程" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import request from '../../api/request'

const auth = useAuthStore()
const tab = ref('all')
const courses = ref([])
const enrolled = ref([])
const router = useRouter()

const subjectLabel = (s) => ({ math: '数学', logic: '逻辑', writing: '写作', english: '英语' }[s] || s)

const load = async () => {
  if (tab.value === 'all') {
    courses.value = (await request.get('/courses')).data
  } else {
    if (!auth.isLoggedIn) {
      enrolled.value = []
      return
    }
    enrolled.value = (await request.get('/courses/enrolled')).data
  }
}

const goLearn = async (c) => {
  const detail = (await request.get(`/courses/${c.id}`)).data
  const first = detail.lessons?.find((l) => l.can_watch)
  if (first) router.push(`/courses/${c.id}/learn/${first.id}`)
  else router.push(`/courses/${c.id}`)
}

onMounted(load)
</script>

<style scoped>
.course-card { cursor: pointer; transition: box-shadow 0.2s; }
.course-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
.subject { font-size: 13px; color: var(--color-text-muted); margin: 8px 0; }
.price-row { margin: 8px 0; }
.orig { text-decoration: line-through; color: var(--color-text-muted); margin-right: 8px; font-size: 13px; }
.now { color: var(--color-error); font-weight: 700; font-size: 18px; }
.login-prompt { padding: 48px; text-align: center; }
.login-prompt p { margin-bottom: 16px; color: var(--color-text-muted); }
</style>
