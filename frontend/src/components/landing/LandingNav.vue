<template>
  <header class="landing-nav" :class="{ scrolled: isScrolled }">
    <div class="landing-container nav-inner">
      <router-link to="/" class="brand">
        <span class="brand-icon">⛵</span>
        <div>
          <div class="brand-name">On-Board 管综方舟</div>
          <div class="brand-sub">管理类联考智能备考平台</div>
        </div>
      </router-link>

      <nav class="nav-links" :class="{ open: menuOpen }">
        <a v-for="link in navLinks" :key="link.href" :href="link.href" @click="menuOpen = false">{{ link.label }}</a>
      </nav>

      <div class="nav-actions">
        <router-link to="/login" class="nav-login">登录</router-link>
        <router-link to="/register/student" class="landing-btn-primary nav-cta">免费体验</router-link>
        <router-link to="/register/teacher" class="nav-teacher">教师入驻</router-link>
        <button class="menu-toggle" @click="menuOpen = !menuOpen" aria-label="菜单">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { navLinks } from '../../data/landing.mock.js'

const isScrolled = ref(false)
const menuOpen = ref(false)

const onScroll = () => { isScrolled.value = window.scrollY > 40 }

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.landing-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  padding: 16px 0;
  transition: background 0.3s, backdrop-filter 0.3s;
}
.landing-nav.scrolled {
  background: rgba(10, 22, 40, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.nav-inner { display: flex; align-items: center; justify-content: space-between; gap: 24px; }
.brand { display: flex; align-items: center; gap: 12px; text-decoration: none; color: #fff; }
.brand-icon { font-size: 28px; }
.brand-name { font-weight: 700; font-size: 17px; }
.brand-sub { font-size: 11px; color: rgba(255,255,255,0.6); margin-top: 2px; }
.nav-links { display: flex; gap: 28px; }
.nav-links a { color: rgba(255,255,255,0.85); text-decoration: none; font-size: 14px; transition: color 0.2s; }
.nav-links a:hover { color: #fff; }
.nav-actions { display: flex; align-items: center; gap: 12px; }
.nav-login { color: rgba(255,255,255,0.9); text-decoration: none; font-size: 14px; }
.nav-cta { padding: 10px 20px; font-size: 14px; }
.nav-teacher {
  color: #fff; text-decoration: none; font-size: 14px;
  border: 1px solid rgba(255,255,255,0.35); border-radius: 10px; padding: 10px 16px;
}
.menu-toggle { display: none; flex-direction: column; gap: 5px; background: none; border: none; cursor: pointer; padding: 4px; }
.menu-toggle span { display: block; width: 22px; height: 2px; background: #fff; }

@media (max-width: 1024px) {
  .nav-links { display: none; position: absolute; top: 100%; left: 0; right: 0; flex-direction: column; background: rgba(10,22,40,0.98); padding: 20px 24px; gap: 16px; }
  .nav-links.open { display: flex; }
  .nav-teacher { display: none; }
  .menu-toggle { display: flex; }
}
</style>
