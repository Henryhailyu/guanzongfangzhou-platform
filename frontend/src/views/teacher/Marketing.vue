<template>
  <div class="marketing-page">
    <h2>营销中心</h2>
    <p class="desc">生成专属推广链接，分享到抖音、微信等渠道。学员通过链接访问后 7 天内购课将记录推广来源。</p>

    <div class="compact-stat-grid">
      <div class="card compact-stat-card">
        <div class="stat-title">推广链接</div>
        <div class="stat-value">{{ marketing.stats?.link_count ?? 0 }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">总点击</div>
        <div class="stat-value">{{ marketing.stats?.total_clicks ?? 0 }}</div>
      </div>
      <div class="card compact-stat-card">
        <div class="stat-title">成交数</div>
        <div class="stat-value">{{ marketing.stats?.total_conversions ?? 0 }}</div>
      </div>
    </div>

    <div class="card section">
      <h3>教师主页</h3>
      <p class="hint">学生可通过主页浏览您的全部课程</p>
      <div class="homepage-row">
        <code class="url">{{ homepageFullUrl }}</code>
        <el-button size="small" @click="copy(homepageFullUrl)">复制链接</el-button>
        <router-link :to="marketing.homepage_url || '#'">
          <el-button size="small" type="primary" link>预览主页</el-button>
        </router-link>
      </div>
      <div v-if="homepageFullUrl" class="qr-wrap">
        <img :src="qrCodeUrl(homepageFullUrl)" alt="主页二维码" class="qr" />
        <span class="qr-hint">微信扫码预览教师主页</span>
      </div>
    </div>

    <div class="card section">
      <div class="section-head">
        <h3>生成推广链接</h3>
        <el-button type="primary" :loading="creating" @click="createLink">生成链接</el-button>
      </div>
      <el-form inline class="link-form">
        <el-form-item label="推广目标">
          <el-select v-model="courseId" placeholder="全店 / 教师主页" clearable style="width: 240px">
            <el-option label="教师主页（全店）" :value="null" />
            <el-option
              v-for="c in marketing.courses || []"
              :key="c.id"
              :label="c.title"
              :value="c.id"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <el-table :data="marketing.links || []" empty-text="还没有推广链接，点击上方生成">
        <el-table-column prop="course_title" label="目标" min-width="140" />
        <el-table-column prop="code" label="推广码" width="100" />
        <el-table-column label="链接" min-width="220">
          <template #default="{ row }">
            <code class="url-sm">{{ fullUrl(row.url) }}</code>
          </template>
        </el-table-column>
        <el-table-column prop="click_count" label="点击" width="70" />
        <el-table-column prop="convert_count" label="成交" width="70" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" link type="primary" @click="copy(fullUrl(row.url))">复制</el-button>
            <el-button size="small" link @click="showQr(row)">二维码</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="qrVisible" title="推广二维码" width="360px" align-center>
      <div v-if="qrTarget" class="qr-dialog">
        <img :src="qrCodeUrl(qrTarget)" alt="推广二维码" class="qr-lg" />
        <p class="qr-url">{{ qrTarget }}</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../api/request'
import { fullUrl, qrCodeUrl } from '../../utils/referral'

const marketing = ref({ links: [], courses: [], stats: {} })
const courseId = ref(null)
const creating = ref(false)
const qrVisible = ref(false)
const qrTarget = ref('')

const homepageFullUrl = computed(() =>
  marketing.value.homepage_url ? fullUrl(marketing.value.homepage_url) : ''
)

const load = async () => {
  marketing.value = (await request.get('/teacher/marketing')).data
}

const copy = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败，请手动复制')
  }
}

const createLink = async () => {
  creating.value = true
  try {
    const res = await request.post('/teacher/marketing/links', {
      course_id: courseId.value || undefined,
    })
    ElMessage.success('推广链接已生成')
    if (res.data?.url) copy(fullUrl(res.data.url))
    await load()
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    creating.value = false
  }
}

const showQr = (row) => {
  qrTarget.value = fullUrl(row.url)
  qrVisible.value = true
}

onMounted(load)
</script>

<style scoped>
.desc { color: var(--color-text-muted); margin: -8px 0 20px; font-size: 14px; }
.section { padding: 24px; margin-top: 20px; }
.section h3 { margin: 0 0 8px; font-size: 16px; }
.hint { font-size: 13px; color: var(--color-text-muted); margin: 0 0 16px; }
.section-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.section-head h3 { margin: 0; }
.homepage-row { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.url { font-size: 13px; background: var(--color-surface); padding: 8px 12px; border-radius: 8px; flex: 1; word-break: break-all; }
.url-sm { font-size: 12px; word-break: break-all; }
.link-form { margin-bottom: 8px; }
.qr-wrap { margin-top: 20px; text-align: center; }
.qr { border-radius: 8px; border: 1px solid var(--color-border); }
.qr-hint { display: block; margin-top: 8px; font-size: 12px; color: var(--color-text-muted); }
.qr-dialog { text-align: center; }
.qr-lg { border-radius: 8px; }
.qr-url { font-size: 12px; color: var(--color-text-muted); word-break: break-all; margin-top: 12px; }
</style>
