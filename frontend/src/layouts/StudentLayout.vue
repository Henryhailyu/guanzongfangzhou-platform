<template>
  <div class="student-layout">
    <header class="header">
      <router-link to="/" class="logo">
        <span class="logo-main">On-Board 管综方舟</span>
      </router-link>
      <nav>
        <router-link to="/practice">刷题</router-link>
        <router-link to="/courses">课程</router-link>
        <router-link to="/wrong-book">错题本</router-link>
        <router-link v-if="auth.isLoggedIn" to="/dashboard">学习中心</router-link>
        <router-link v-if="auth.isLoggedIn" to="/points">积分</router-link>
        <router-link v-if="auth.isLoggedIn" to="/orders">订单</router-link>
        <router-link v-if="!auth.isLoggedIn" to="/login">登录</router-link>
        <a v-else href="#" @click.prevent="logout">退出</a>
      </nav>
    </header>
    <main class="main"><router-view /></main>
    <footer class="footer">© 2026 On-Board 管综方舟</footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const logout = () => { auth.logout(); router.push('/') }
</script>

<style scoped>
.header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 32px; background: #fff; border-bottom: 1px solid var(--color-border);
}
.logo { font-weight: 700; font-size: 18px; color: var(--color-text-main); }
nav a { margin-left: 24px; color: var(--color-text-muted); }
nav a.router-link-active { color: var(--color-primary); font-weight: 500; }
.main { max-width: 1100px; margin: 0 auto; padding: 48px 24px; min-height: 70vh; }
.footer { text-align: center; padding: 32px; color: var(--color-text-muted); font-size: 14px; }
</style>
