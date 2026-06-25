<template>
  <div class="practice-page">
    <el-alert
      v-if="quota.quota_used && !quota.unlimited"
      type="warning"
      :closable="false"
      show-icon
      class="quota-banner"
      title="今日免费额度已用尽，继续刷题每题消耗 5 积分"
    >
      <template #default>
        <router-link to="/points">查看积分中心</router-link>
      </template>
    </el-alert>
    <div v-else-if="quota.remaining_free !== undefined && !quota.unlimited" class="quota-hint card">
      今日免费剩余 <strong>{{ quota.remaining_free }}</strong> 题 · 积分余额 <strong>{{ balance }}</strong>
      <router-link to="/points">积分中心</router-link>
    </div>

    <div class="toolbar card">
      <div class="toolbar-row">
        <el-select v-model="subject" style="width:140px" @change="onSubjectChange">
          <el-option label="数学基础" value="math" />
          <el-option label="逻辑推理" value="logic" />
        </el-select>
        <el-radio-group v-model="mode" @change="loadSet">
          <el-radio-button value="random">随机练习</el-radio-button>
          <el-radio-button value="specialized">专项练习</el-radio-button>
        </el-radio-group>
        <el-select
          v-if="mode === 'specialized'"
          v-model="tag"
          placeholder="选择知识点"
          style="width:160px"
          @change="loadSet"
        >
          <el-option v-for="t in tags" :key="t" :label="t" :value="t" />
        </el-select>
        <el-button type="primary" @click="loadSet">开始练习</el-button>
      </div>
      <div v-if="questions.length" class="progress-row">
        <span>进度 {{ currentIndex + 1 }} / {{ questions.length }}</span>
        <el-progress :percentage="progressPct" :stroke-width="8" style="flex:1;margin:0 16px" />
        <span class="timer">⏱ {{ formatTime(elapsed) }}</span>
      </div>
    </div>

    <div v-if="current" class="card question-card">
      <div class="meta">
        <el-tag size="small">{{ subjectLabel }}</el-tag>
        <el-tag v-if="current.tags?.primary" size="small" type="info">{{ current.tags.primary }}</el-tag>
        <el-tag size="small" type="warning">难度 {{ current.difficulty || 1 }}</el-tag>
      </div>
      <p class="stem">{{ current.content.stem }}</p>
      <el-radio-group v-model="answer" class="options" :disabled="!!result">
        <el-radio v-for="opt in current.content.options" :key="opt" :value="opt[0]">{{ opt }}</el-radio>
      </el-radio-group>

      <div class="actions">
        <el-button v-if="!result" type="primary" :loading="submitting" :disabled="!answer" @click="submit">
          提交答案
        </el-button>
        <el-button v-else type="primary" @click="nextQuestion">下一题 →</el-button>
      </div>

      <div v-if="result" class="result" :class="{ ok: result.is_correct }">
        <strong>{{ result.is_correct ? '✓ 回答正确' : `✕ 回答错误，正确答案：${result.correct_answer}` }}</strong>
        <p v-if="result.analysis">{{ result.analysis }}</p>
        <small>
          <template v-if="result.points_cost">-{{ result.points_cost }} 积分 · </template>
          +{{ result.points_earned }} 积分 · 余额 {{ result.balance }}
        </small>
        <div v-if="result.similar_questions?.length" class="similar">
          <div class="similar-title">同类题推荐</div>
          <div v-for="s in result.similar_questions" :key="s.question_id" class="similar-item">
            {{ s.content.stem }}
          </div>
        </div>
      </div>
    </div>

    <el-empty v-else-if="loaded" description="暂无题目，请切换科目或知识点" />
    <div v-else class="hint card">选择科目和练习模式，点击「开始练习」</div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../api/request'

const router = useRouter()
const subject = ref('math')
const mode = ref('random')
const tag = ref('')
const tags = ref([])
const questions = ref([])
const currentIndex = ref(0)
const answer = ref('')
const submitting = ref(false)
const result = ref(null)
const loaded = ref(false)
const elapsed = ref(0)
const quota = ref({})
const balance = ref(0)
let timer = null
let startAt = null

const subjectLabel = computed(() => ({ math: '数学基础', logic: '逻辑推理' }[subject.value]))
const current = computed(() => questions.value[currentIndex.value])
const progressPct = computed(() =>
  questions.value.length ? Math.round(((currentIndex.value + (result.value ? 1 : 0)) / questions.value.length) * 100) : 0
)

const formatTime = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`

const startTimer = () => {
  stopTimer()
  startAt = Date.now()
  elapsed.value = 0
  timer = setInterval(() => { elapsed.value = Math.floor((Date.now() - startAt) / 1000) }, 1000)
}

const stopTimer = () => {
  if (timer) { clearInterval(timer); timer = null }
}

const loadTags = async () => {
  tags.value = (await request.get('/questions/tags', { params: { subject: subject.value } })).data
  if (tags.value.length && !tags.value.includes(tag.value)) tag.value = tags.value[0]
}

const onSubjectChange = async () => {
  await loadTags()
  loadSet()
}

const loadSet = async () => {
  loaded.value = true
  result.value = null
  answer.value = ''
  currentIndex.value = 0
  try {
    const res = await request.get('/questions/practice', {
      params: {
        subject: subject.value,
        mode: mode.value,
        tag: mode.value === 'specialized' ? tag.value : undefined,
        count: 10,
      },
    })
    questions.value = res.data.items || res.data
    if (!questions.value.length) ElMessage.info('该条件下暂无题目')
    else startTimer()
  } catch (e) {
    ElMessage.error(e.message || '加载失败')
    questions.value = []
  }
}

const submit = async () => {
  if (!current.value || !answer.value) return
  submitting.value = true
  try {
    const res = await request.post(`/questions/${current.value.question_id}/submit`, {
      answer: answer.value,
      time_spent: elapsed.value || 1,
    })
    result.value = res.data
    balance.value = res.data.balance
    stopTimer()
    loadQuota()
  } catch (e) {
    const msg = e.message || '提交失败'
    if (msg.includes('额度') || msg.includes('积分不足')) {
      ElMessageBox.confirm(
        '今日免费刷题额度已用尽且积分不足。可前往积分中心签到获取积分，或明日再来。',
        '无法继续刷题',
        { confirmButtonText: '积分中心', cancelButtonText: '知道了', type: 'warning' }
      ).then(() => router.push('/points')).catch(() => {})
    } else {
      ElMessage.error(msg)
    }
  } finally {
    submitting.value = false
  }
}

const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value += 1
    answer.value = ''
    result.value = null
    startTimer()
  } else {
    ElMessage.success('本轮练习完成！')
    loadSet()
  }
}

onMounted(async () => {
  await loadTags()
  loadQuota()
})

const loadQuota = async () => {
  try {
    const [q, b] = await Promise.all([
      request.get('/points/quota/today'),
      request.get('/points/balance'),
    ])
    quota.value = q.data
    balance.value = b.data.points
  } catch { /* guest or error */ }
}

onUnmounted(stopTimer)
</script>

<style scoped>
.practice-page { display: flex; flex-direction: column; gap: 20px; }
.quota-banner { margin-bottom: 0; }
.quota-hint {
  padding: 12px 16px; font-size: 14px; color: var(--color-text-muted);
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
}
.quota-hint a { margin-left: auto; font-size: 13px; }
.toolbar { padding: 20px; }
.toolbar-row { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.progress-row { display: flex; align-items: center; margin-top: 16px; font-size: 14px; color: var(--color-text-muted); }
.timer { font-variant-numeric: tabular-nums; min-width: 56px; }
.question-card { padding: 28px; }
.meta { display: flex; gap: 8px; margin-bottom: 16px; }
.stem { font-size: 18px; line-height: 1.8; margin: 0 0 8px; }
.options { display: flex; flex-direction: column; align-items: flex-start; gap: 14px; margin: 24px 0; }
.actions { margin-top: 8px; }
.result { margin-top: 20px; padding: 20px; border-radius: 12px; background: #fef2f2; line-height: 1.7; }
.result.ok { background: #ecfdf5; }
.result p { margin: 8px 0; color: #374151; }
.similar { margin-top: 16px; padding-top: 16px; border-top: 1px dashed #d1d5db; }
.similar-title { font-size: 13px; color: var(--color-text-muted); margin-bottom: 8px; }
.similar-item { font-size: 14px; padding: 8px 0; color: #4b5563; }
.hint { padding: 48px; text-align: center; color: var(--color-text-muted); }
</style>
