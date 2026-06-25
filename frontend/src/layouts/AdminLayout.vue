<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="brand">管理后台</div>
      <router-link to="/admin">数据看板</router-link>
      <router-link to="/admin/users">用户管理</router-link>
      <router-link to="/admin/teachers">教师审核</router-link>
      <router-link to="/admin/courses">课程管理</router-link>
      <router-link to="/admin/orders">订单管理</router-link>
      <a href="#" class="logout" @click.prevent="logout">退出</a>
    </aside>
    <main class="content"><router-view /></main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
const auth = useAuthStore()
const router = useRouter()
const logout = () => { auth.logout(); router.push('/login') }
</script>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; }
.sidebar {
  width: 220px; background: #1a1a2e; padding: 24px 16px;
  display: flex; flex-direction: column; gap: 8px;
}
.brand { font-weight: 700; margin-bottom: 24px; color: #fff; }
.sidebar a { padding: 10px 12px; border-radius: 8px; color: #9ca3af; }
.sidebar a.router-link-active { background: rgba(79,110,247,0.3); color: #fff; }
.logout { margin-top: auto; color: #9ca3af; }
.content { flex: 1; padding: 32px; background: var(--color-surface); }
</style>
