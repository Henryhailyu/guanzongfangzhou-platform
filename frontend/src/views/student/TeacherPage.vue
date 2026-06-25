<template>
  <div v-if="data" class="teacher-page">
    <div class="hero card">
      <div class="avatar">{{ avatarLetter }}</div>
      <div class="info">
        <h1>{{ data.teacher.real_name || data.teacher.nickname }}</h1>
        <p v-if="data.teacher.expertise" class="expertise">擅长：{{ data.teacher.expertise }}</p>
        <p class="bio">{{ data.teacher.bio || '这位老师还没有填写简介。' }}</p>
        <div class="stats">
          <span>{{ data.stats.course_count }} 门课程</span>
          <span>{{ data.stats.student_count }} 名学员</span>
        </div>
      </div>
    </div>

    <h2>在售课程</h2>
    <div class="compact-stat-grid">
      <div
        v-for="c in data.courses"
        :key="c.id"
        class="card compact-stat-card course-card"
        @click="goCourse(c.id)"
      >
        <el-tag size="small">{{ subjectLabel(c.subject) }}</el-tag>
        <div class="stat-title">{{ c.title }}</div>
        <p class="desc">{{ c.description }}</p>
        <div class="meta">{{ c.total_lessons }} 课时 · {{ c.student_count }} 人学习</div>
        <div class="price">
          {{ c.is_free || c.price === 0 ? '免费' : `¥${c.price}` }}
        </div>
      </div>
    </div>
    <el-empty v-if="!data.courses.length" description="暂无在售课程" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '../../api/request'
import { captureReferral } from '../../utils/referral'

const route = useRoute()
const router = useRouter()
const data = ref(null)

const subjectLabel = (s) => ({
  math: '数学', logic: '逻辑', writing: '写作', english: '英语', combo: '综合',
}[s] || s)

const avatarLetter = computed(() => {
  const name = data.value?.teacher?.real_name || data.value?.teacher?.nickname || '师'
  return name[0]
})

const refCode = computed(() => route.query.ref || '')

const goCourse = (id) => {
  const query = refCode.value ? { ref: refCode.value } : undefined
  router.push({ path: `/courses/${id}`, query })
}

onMounted(async () => {
  if (route.query.ref) captureReferral(String(route.query.ref))
  data.value = (await request.get(`/teachers/${route.params.slug}`)).data
})
</script>

<style scoped>
.teacher-page { display: flex; flex-direction: column; gap: 24px; }
.hero { display: flex; gap: 24px; padding: 28px; align-items: flex-start; }
.avatar {
  width: 88px; height: 88px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, var(--color-primary), #8B5CF6);
  color: #fff; font-size: 36px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.info h1 { margin: 0 0 8px; font-size: 24px; }
.expertise { color: var(--color-primary); font-size: 14px; margin: 0 0 12px; }
.bio { color: var(--color-text-muted); line-height: 1.7; margin: 0 0 16px; }
.stats { display: flex; gap: 20px; font-size: 14px; color: var(--color-text-muted); }
.course-card { cursor: pointer; transition: box-shadow 0.2s; }
.course-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
.desc {
  font-size: 13px; color: var(--color-text-muted); margin: 8px 0;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.meta { font-size: 12px; color: var(--color-text-muted); }
.price { margin-top: 12px; font-size: 20px; font-weight: 700; color: var(--color-primary); }
@media (max-width: 640px) { .hero { flex-direction: column; align-items: center; text-align: center; } }
</style>
