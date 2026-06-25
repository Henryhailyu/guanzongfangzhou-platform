<template>
  <div class="auth-card card">
    <h2>考生注册</h2>
    <p class="desc">注册后即可使用智能题库、学习看板与名师课程。</p>
    <el-form @submit.prevent="onSubmit" label-position="top">
      <el-form-item label="昵称">
        <el-input v-model="form.nickname" placeholder="你的称呼" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="form.email" type="email" placeholder="用于登录" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" show-password placeholder="至少 6 位" />
      </el-form-item>
      <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">注册并开始备考</el-button>
    </el-form>
    <p class="footer-link">已有账号？<router-link to="/login">登录</router-link></p>
    <p class="footer-link alt">我是老师，<router-link to="/register/teacher">申请入驻</router-link></p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'

const form = reactive({ nickname: '', email: '', password: '' })
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

const onSubmit = async () => {
  if (!form.email || !form.password) return ElMessage.warning('请填写邮箱和密码')
  if (form.password.length < 6) return ElMessage.warning('密码至少 6 位')
  loading.value = true
  try {
    await auth.register({ ...form, role: 'student' })
    ElMessage.success('注册成功')
    router.push('/dashboard')
  } catch (e) {
    ElMessage.error(e.message || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-card { width: 420px; max-width: 100%; padding: 32px; }
.desc { color: var(--color-text-muted); font-size: 14px; margin: -8px 0 24px; }
.footer-link { margin-top: 16px; font-size: 14px; color: var(--color-text-muted); text-align: center; }
.footer-link.alt { margin-top: 8px; font-size: 13px; }
</style>
