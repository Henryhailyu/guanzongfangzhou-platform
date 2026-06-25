<template>
  <div>
    <h2>系统设置</h2>
    <p class="desc">配置免费刷题额度、AI 积分消耗与分销规则，保存后立即生效。</p>

    <el-form v-loading="loading" label-width="200px" class="settings-form">
      <section class="card section">
        <h3>刷题额度</h3>
        <el-form-item label="每日免费题数">
          <el-input-number v-model="form.quota.free_daily_questions" :min="1" :max="200" />
        </el-form-item>
        <el-form-item label="答错扣减额度">
          <el-input-number v-model="form.quota.wrong_quota_penalty" :min="0" :max="20" />
        </el-form-item>
        <el-form-item label="答错几次用尽额度">
          <el-input-number v-model="form.quota.max_wrong_before_quota" :min="1" :max="20" />
        </el-form-item>
        <el-form-item label="超额后每题积分">
          <el-input-number v-model="form.quota.points_per_question_after_quota" :min="1" :max="50" />
        </el-form-item>
      </section>

      <section class="card section">
        <h3>AI 功能积分</h3>
        <el-form-item label="写作批改（每次）">
          <el-input-number v-model="form.ai.writing_points" :min="1" :max="500" />
        </el-form-item>
        <el-form-item label="视频解析（每次）">
          <el-input-number v-model="form.ai.video_analysis_points" :min="1" :max="100" />
        </el-form-item>
      </section>

      <section class="card section">
        <h3>分销规则</h3>
        <el-form-item label="默认佣金比例">
          <el-input-number v-model="form.referral.default_commission_rate" :min="0" :max="1" :step="0.01" :precision="2" />
          <span class="hint">0.10 = 10%</span>
        </el-form-item>
        <el-form-item label="最高佣金比例">
          <el-input-number v-model="form.referral.max_commission_rate" :min="0" :max="1" :step="0.01" :precision="2" />
        </el-form-item>
        <el-form-item label="最低提现金额（元）">
          <el-input-number v-model="form.referral.withdraw_min_amount" :min="1" :max="10000" />
        </el-form-item>
      </section>

      <el-button type="primary" :loading="saving" @click="save">保存设置</el-button>
    </el-form>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../api/request'

const loading = ref(false)
const saving = ref(false)
const form = reactive({
  quota: {
    free_daily_questions: 20,
    wrong_quota_penalty: 5,
    max_wrong_before_quota: 5,
    points_per_question_after_quota: 5,
  },
  ai: { writing_points: 50, video_analysis_points: 10 },
  referral: {
    default_commission_rate: 0.1,
    max_commission_rate: 0.2,
    withdraw_min_amount: 50,
  },
})

const load = async () => {
  loading.value = true
  try {
    const data = (await request.get('/admin/settings')).data
    Object.assign(form.quota, data.quota)
    Object.assign(form.ai, data.ai)
    Object.assign(form.referral, data.referral)
  } finally {
    loading.value = false
  }
}

const save = async () => {
  saving.value = true
  try {
    await request.put('/admin/settings', {
      quota: { ...form.quota },
      ai: { ...form.ai },
      referral: { ...form.referral },
    })
    ElMessage.success('系统配置已保存')
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.desc { color: var(--color-text-secondary, #6b7280); margin: 8px 0 20px; }
.settings-form { max-width: 640px; }
.section { padding: 20px 24px; margin-bottom: 20px; }
.section h3 { margin: 0 0 16px; font-size: 16px; }
.hint { margin-left: 12px; color: #9ca3af; font-size: 13px; }
</style>
