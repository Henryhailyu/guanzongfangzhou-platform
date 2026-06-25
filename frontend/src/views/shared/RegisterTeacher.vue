<template>
  <div class="auth-card card">
    <h2>教师入驻申请</h2>
    <p class="desc">提交资料后由平台管理员审核，通过即可开课售课。</p>
    <el-form @submit.prevent="onSubmit" label-position="top">
      <el-form-item label="真实姓名">
        <el-input v-model="form.real_name" placeholder="与证件一致" />
      </el-form-item>
      <el-form-item label="擅长科目">
        <el-select v-model="form.expertise" placeholder="选择主授科目" style="width:100%">
          <el-option label="数学基础" value="math" />
          <el-option label="逻辑推理" value="logic" />
          <el-option label="写作" value="writing" />
          <el-option label="英语二" value="english" />
          <el-option label="综合" value="combo" />
        </el-select>
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="form.email" type="email" placeholder="用于登录" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" show-password placeholder="至少 6 位" />
      </el-form-item>
      <el-form-item label="个人简介（选填）">
        <el-input v-model="form.bio" type="textarea" :rows="3" placeholder="教学经历、授课风格等" />
      </el-form-item>
      <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">提交入驻申请</el-button>
    </el-form>
    <p class="footer-link">已有账号？<router-link to="/login">登录</router-link></p>
    <p class="footer-link alt">我是考生，<router-link to="/register/student">去注册</router-link></p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'

const form = reactive({ real_name: '', expertise: '', email: '', password: '', bio: '' })
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

const onSubmit = async () => {
  if (!form.real_name || !form.expertise || !form.email || !form.password) {
    return ElMessage.warning('请填写必填项')
  }
  if (form.password.length < 6) return ElMessage.warning('密码至少 6 位')
  loading.value = true
  try {
    await auth.register({
      role: 'teacher',
      nickname: form.real_name,
      email: form.email,
      password: form.password,
      real_name: form.real_name,
      expertise: form.expertise,
      bio: form.bio,
    })
    ElMessage.success('申请已提交，请等待管理员审核')
    router.push('/teacher')
  } catch (e) {
    ElMessage.error(e.message || '提交失败')
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
