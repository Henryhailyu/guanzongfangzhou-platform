<template>
  <div v-if="course" class="detail">
    <div class="header card">
      <div>
        <el-tag size="small">{{ course.subject_label || course.subject }}</el-tag>
        <h2>{{ course.title }}</h2>
        <p class="desc">{{ course.description }}</p>
        <p class="meta">{{ course.teacher_name }} · {{ course.student_count }} 人学习 · {{ course.lessons?.length || 0 }} 课时</p>
      </div>
      <div class="buy-box">
        <div class="price">
          <span v-if="course.original_price" class="orig">¥{{ course.original_price }}</span>
          <span class="now">{{ isFree ? '免费' : `¥${course.price}` }}</span>
        </div>
        <el-button v-if="course.enrolled" type="primary" @click="goLearn">进入学习</el-button>
        <el-button v-else-if="isFree" type="primary" :loading="enrolling" @click="enrollFree">免费加入</el-button>
        <el-button v-else type="primary" @click="openCheckout">购买课程</el-button>
        <p v-if="course.enrolled" class="enrolled-tip">已购买 · 进度 {{ course.progress_pct }}%</p>
      </div>
    </div>

    <h3>课程目录</h3>
    <div class="lesson-list">
      <div
        v-for="l in course.lessons"
        :key="l.id"
        class="card lesson-item"
        :class="{ locked: !l.can_watch }"
        @click="openLesson(l)"
      >
        <div class="lesson-title">
          <span>{{ l.title }}</span>
          <el-tag v-if="l.is_free" size="small" type="success">试看</el-tag>
          <el-tag v-else-if="!l.can_watch" size="small" type="info">需购买</el-tag>
        </div>
        <span class="action">{{ l.can_watch ? '播放 →' : '🔒' }}</span>
      </div>
    </div>

    <CheckoutDialog
      :visible="checkoutVisible"
      product-type="course"
      :product-id="course.id"
      :product-title="course.title"
      :amount="course.price"
      :points-granted="Math.max(1, Math.floor(course.price / 10))"
      :referral-code="referralCode"
      title="购买课程"
      @close="checkoutVisible = false"
      @success="onPaid"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'
import request from '../../api/request'
import CheckoutDialog from '../../components/CheckoutDialog.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const course = ref(null)
const enrolling = ref(false)
const checkoutVisible = ref(false)
const referralCode = computed(() => route.query.ref || '')

const isFree = computed(() => course.value?.is_free || course.value?.price === 0)

const load = async () => {
  course.value = (await request.get(`/courses/${route.params.id}`)).data
}

const goLearn = () => {
  const first = course.value.lessons?.find((l) => l.can_watch)
  if (first) router.push(`/courses/${course.value.id}/learn/${first.id}`)
}

const openLesson = (l) => {
  if (!l.can_watch) return ElMessage.warning('请先购买课程')
  router.push(`/courses/${course.value.id}/learn/${l.id}`)
}

const enrollFree = async () => {
  enrolling.value = true
  try {
    await request.post(`/courses/${course.value.id}/enroll-free`)
    ElMessage.success('已加入课程')
    await load()
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    enrolling.value = false
  }
}

const openCheckout = () => {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    return router.push({ path: '/login', query: { redirect: route.fullPath } })
  }
  checkoutVisible.value = true
}

const onPaid = async () => {
  checkoutVisible.value = false
  ElMessage.success('购买成功')
  await load()
}

onMounted(load)
</script>

<style scoped>
.header { display: flex; justify-content: space-between; gap: 32px; padding: 28px; margin-bottom: 24px; }
.desc { color: var(--color-text-muted); line-height: 1.7; margin: 12px 0; }
.meta { font-size: 14px; color: var(--color-text-muted); }
.buy-box { text-align: right; flex-shrink: 0; }
.price .now { font-size: 28px; font-weight: 700; color: var(--color-primary); }
.orig { text-decoration: line-through; color: var(--color-text-muted); margin-right: 8px; }
.enrolled-tip { font-size: 13px; color: var(--color-success); margin-top: 8px; }
.lesson-list { display: flex; flex-direction: column; gap: 10px; }
.lesson-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 20px; cursor: pointer; transition: background 0.2s;
}
.lesson-item:hover:not(.locked) { background: var(--color-primary-light); }
.lesson-item.locked { opacity: 0.6; cursor: not-allowed; }
.lesson-title { display: flex; align-items: center; gap: 10px; }
.action { font-size: 14px; color: var(--color-primary); }
@media (max-width: 768px) { .header { flex-direction: column; } .buy-box { text-align: left; } }
</style>
