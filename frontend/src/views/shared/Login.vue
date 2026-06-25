<template>
  <div class="auth-card card">
    <h2>登录</h2>
    <p class="desc">登录后根据账号角色进入对应工作台。</p>
    <el-form @submit.prevent="onSubmit" label-position="top">
      <el-form-item label="账号">
        <el-input v-model="account" placeholder="邮箱或手机号" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input ref="passwordInput" v-model="password" type="password" show-password />
      </el-form-item>
      <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">登录</el-button>
    </el-form>
    <div class="register-links">
      <router-link to="/register/student" class="reg-btn student">考生注册 →</router-link>
      <router-link to="/register/teacher" class="reg-btn teacher">教师入驻 →</router-link>
    </div>
    <p class="hint">
      测试账号：student@guanlian.com / student123 · teacher@guanlian.com / teacher123 · admin@guanlian.com / admin123
    </p>
    <p class="hint admin-hint">
      管理员请点击下方按钮，在上方表单输入账号密码后登录：
    </p>
    <el-button class="admin-entry-btn" type="primary" plain @click="prepareAdminLogin">
      管理员登录
    </el-button>
    <el-button
      v-if="auth.isLoggedIn && auth.role === 'admin'"
      class="admin-entry-btn"
      type="primary"
      @click="router.push('/admin')"
    >
      已登录，直接进入管理后台
    </el-button>
  </div>
</template>

<script setup>
import { nextTick, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'

const account = ref('')
const password = ref('')
const passwordInput = ref(null)
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const onSubmit = async () => {
  loading.value = true
  try {
    await auth.login(account.value, password.value)
    ElMessage.success('登录成功')
    const redirect = route.query.redirect
    if (redirect) router.push(redirect)
    else auth.redirectByRole(router)
  } catch (e) {
    ElMessage.error(e.message || '登录失败')
  } finally {
    loading.value = false
  }
}

const prepareAdminLogin = async () => {
  if (auth.isLoggedIn && auth.role !== 'admin') {
    ElMessage.warning('当前已登录其他角色，请先退出后再登录管理员账号')
    return
  }
  if (auth.isLoggedIn && auth.role === 'admin') {
    auth.logout()
  }
  if (route.query.redirect !== '/admin') {
    await router.replace({ path: '/login', query: { redirect: '/admin' } })
  }
  account.value = 'admin@guanlian.com'
  password.value = ''
  await nextTick()
  passwordInput.value?.focus?.()
  ElMessage.info('请输入管理员密码，然后点击上方「登录」')
}
</script>

<style scoped>
.auth-card { width: 420px; max-width: 100%; padding: 32px; }
.desc { color: var(--color-text-muted); font-size: 14px; margin: -8px 0 24px; }
.register-links { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px; }
.reg-btn {
  display: block; text-align: center; padding: 12px; border-radius: 10px;
  font-size: 14px; text-decoration: none; transition: all 0.2s;
}
.reg-btn.student { background: var(--color-primary-light); color: var(--color-primary); }
.reg-btn.teacher { border: 1px solid var(--color-border); color: var(--color-text-muted); }
.reg-btn:hover { opacity: 0.9; }
.hint { margin-top: 20px; font-size: 12px; color: var(--color-text-muted); line-height: 1.6; }
.admin-hint { margin-top: 8px; margin-bottom: 12px; }
.admin-entry-btn { width: 100%; margin-top: 8px; }
.admin-entry-btn + .admin-entry-btn { margin-top: 8px; }
</style>
