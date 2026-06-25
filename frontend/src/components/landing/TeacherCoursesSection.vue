<template>
  <section class="landing-section section-light" id="courses">
    <div class="landing-container">
      <div class="section-heading">
        <h2>找到适合你的老师，而不是盲目跟风报班。</h2>
      </div>
      <div class="grid-3">
        <div v-for="t in teachers" :key="t.id || t.name" class="teacher-card">
          <div class="avatar">{{ t.avatar || t.teacher_name?.[0] || t.name?.[0] }}</div>
          <h3>{{ t.teacher_name || t.name }}</h3>
          <div class="subject">{{ subjectLabels[t.subject] || t.subject }}</div>
          <p class="course">{{ t.title || t.course }}</p>
          <div class="tags">
            <span v-for="tag in (t.tags || defaultTags)" :key="tag">{{ tag }}</span>
          </div>
          <div class="actions">
            <router-link
              v-if="t.teacher_slug"
              :to="`/teachers/${t.teacher_slug}`"
              class="btn-outline"
            >教师主页</router-link>
            <router-link v-if="t.id" :to="`/courses/${t.id}`" class="btn-solid">查看课程</router-link>
            <router-link v-else to="/courses" class="btn-solid">查看课程</router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../../api/request'
import { teacherCardsFallback, subjectLabels } from '../../data/landing.mock.js'

const teachers = ref([])
const defaultTags = ['基础强化', '冲刺提分']

onMounted(async () => {
  try {
    const res = await request.get('/courses')
    const list = (res.data || []).slice(0, 3).map((c) => ({
      ...c,
      avatar: c.teacher_name?.[0] || '师',
      tags: defaultTags,
    }))
    teachers.value = list.length ? list : teacherCardsFallback
  } catch {
    teachers.value = teacherCardsFallback
  }
})
</script>

<style scoped>
.teacher-card {
  background: #fff; border: 1px solid #e8eaed; border-radius: 16px;
  padding: 28px; text-align: center; transition: transform 0.25s, box-shadow 0.25s;
}
.teacher-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.08); }
.avatar {
  width: 72px; height: 72px; border-radius: 50%; margin: 0 auto 16px;
  background: linear-gradient(135deg, #4F6EF7, #8B5CF6);
  color: #fff; font-size: 28px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.teacher-card h3 { margin: 0 0 4px; font-size: 18px; color: #1a1a2e; }
.subject { font-size: 13px; color: var(--color-primary); margin-bottom: 12px; }
.course { font-size: 14px; color: #6b7280; margin: 0 0 16px; min-height: 42px; }
.tags { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 20px; }
.tags span { font-size: 12px; padding: 4px 10px; border-radius: 6px; background: #f3f4f6; color: #6b7280; }
.actions { display: flex; gap: 10px; justify-content: center; }
.btn-outline, .btn-solid {
  padding: 10px 18px; border-radius: 10px; font-size: 14px; text-decoration: none; transition: all 0.2s;
}
.btn-outline { border: 1px solid var(--color-primary); color: var(--color-primary); }
.btn-solid { background: var(--color-primary); color: #fff; }
.btn-outline:hover { background: var(--color-primary-light); }
.btn-solid:hover { background: var(--color-primary-hover); color: #fff; }
</style>
