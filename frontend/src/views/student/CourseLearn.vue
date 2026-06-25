<template>
  <div v-if="lesson" class="learn-page">
    <div class="top-bar">
      <router-link :to="`/courses/${courseId}`" class="back">← 返回课程</router-link>
      <span class="title">{{ lesson.course_title }} · {{ lesson.title }}</span>
      <el-tag v-if="lesson.mode === 'preview'" size="small" type="success">试看</el-tag>
    </div>

    <div class="layout">
      <div class="player card">
        <div v-if="lesson.is_mock_player" class="mock-player">
          <div class="mock-icon">▶</div>
          <p>视频播放区（腾讯云 VOD 接入后替换）</p>
          <p class="mock-id">课时 ID: {{ lesson.id }}</p>
          <el-button type="primary" @click="markProgress">标记本节已学完</el-button>
        </div>
        <video v-else-if="lesson.play_url && !lesson.play_url.startsWith('mock://')" controls class="video" :src="lesson.play_url" />
        <div v-else class="mock-player">
          <div class="mock-icon">▶</div>
          <p>Mock 播放</p>
          <el-button type="primary" @click="markProgress">标记本节已学完</el-button>
        </div>
      </div>

      <aside class="sidebar card">
        <h4>课程目录</h4>
        <div
          v-for="l in lesson.lessons"
          :key="l.id"
          class="lesson-row"
          :class="{ active: l.id === lesson.id, locked: !l.can_watch }"
          @click="switchLesson(l)"
        >
          <span>{{ l.title }}</span>
          <el-tag v-if="l.is_free" size="small">试看</el-tag>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../../api/request'

const route = useRoute()
const router = useRouter()
const lesson = ref(null)
const courseId = route.params.id

const loadLesson = async (lessonId) => {
  lesson.value = (await request.get(`/courses/${courseId}/lessons/${lessonId}`)).data
}

const switchLesson = (l) => {
  if (!l.can_watch) return ElMessage.warning('请先购买课程')
  router.push(`/courses/${courseId}/learn/${l.id}`)
}

const markProgress = async () => {
  try {
    const res = await request.post(`/courses/${courseId}/lessons/${lesson.value.id}/progress`)
    ElMessage.success(`学习进度已更新至 ${res.data.progress_pct}%`)
  } catch (e) {
    ElMessage.error(e.message)
  }
}

onMounted(() => {
  const lid = route.params.lessonId || route.query.lesson
  if (lid) loadLesson(lid)
  else ElMessage.warning('请选择课时')
})

watch(() => route.params.lessonId, (id) => { if (id) loadLesson(id) })
</script>

<style scoped>
.learn-page { display: flex; flex-direction: column; gap: 16px; }
.top-bar { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.back { font-size: 14px; color: var(--color-text-muted); }
.title { font-weight: 600; flex: 1; }
.layout { display: grid; grid-template-columns: 1fr 280px; gap: 20px; }
.player { padding: 0; overflow: hidden; }
.mock-player {
  aspect-ratio: 16/9; background: #1a1a2e; color: #fff;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px;
}
.mock-icon { font-size: 48px; opacity: 0.8; }
.mock-id { font-size: 12px; opacity: 0.5; }
.video { width: 100%; display: block; background: #000; }
.sidebar { padding: 16px; max-height: 480px; overflow-y: auto; }
.sidebar h4 { margin: 0 0 12px; font-size: 15px; }
.lesson-row {
  padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 14px;
  display: flex; justify-content: space-between; align-items: center; gap: 8px;
}
.lesson-row:hover:not(.locked) { background: var(--color-primary-light); }
.lesson-row.active { background: var(--color-primary-light); color: var(--color-primary); font-weight: 500; }
.lesson-row.locked { opacity: 0.5; cursor: not-allowed; }
@media (max-width: 900px) { .layout { grid-template-columns: 1fr; } }
</style>
