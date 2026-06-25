<template>
  <div class="teacher-layout">
    <aside class="sidebar">
      <div class="brand">教师工作台</div>
      <el-alert
        v-if="status === 'pending'"
        title="入驻审核中"
        description="管理员审核通过后即可创建课程。"
        type="warning"
        :closable="false"
        show-icon
        class="status-alert"
      />
      <el-alert
        v-else-if="status === 'rejected'"
        title="入驻申请未通过"
        description="如有疑问请联系平台管理员。"
        type="error"
        :closable="false"
        show-icon
        class="status-alert"
      />
      <el-alert
        v-else-if="status === 'suspended'"
        title="账号已暂停"
        description="请联系平台管理员恢复权限。"
        type="error"
        :closable="false"
        show-icon
        class="status-alert"
      />
      <router-link to="/teacher" :class="{ disabled: !approved }">概览</router-link>
      <router-link to="/teacher/courses" :class="{ disabled: !approved }" @click="blockIfPending">我的课程</router-link>
      <router-link to="/teacher/students" :class="{ disabled: !approved }" @click="blockIfPending">我的学员</router-link>
      <router-link to="/teacher/marketing" :class="{ disabled: !approved }" @click="blockIfPending">营销中心</router-link>
      <a href="#" class="logout" @click.prevent="logout">退出</a>
    </aside>
    <main class="content"><router-view /></main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const status = computed(() => auth.teacherStatus)
const approved = computed(() => auth.isApprovedTeacher)

onMounted(() => auth.fetchMe())

const blockIfPending = (e) => {
  if (!approved.value) {
    e.preventDefault()
    ElMessage.warning('教师账号审核通过后可使用此功能')
  }
}

const logout = () => { auth.logout(); router.push('/login') }
</script>

<style scoped>
.teacher-layout { display: flex; min-height: 100vh; }
.sidebar {
  width: 220px; background: #fff; border-right: 1px solid var(--color-border);
  padding: 24px 16px; display: flex; flex-direction: column; gap: 8px;
}
.brand { font-weight: 700; margin-bottom: 16px; color: var(--color-primary); }
.status-alert { margin-bottom: 12px; }
.sidebar a { padding: 10px 12px; border-radius: 8px; color: var(--color-text-muted); }
.sidebar a.router-link-active { background: var(--color-primary-light); color: var(--color-primary); }
.sidebar a.disabled:not(.router-link-active) { opacity: 0.45; pointer-events: none; }
.logout { margin-top: auto; }
.content { flex: 1; padding: 32px; }
</style>
