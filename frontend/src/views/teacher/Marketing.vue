<template>
  <div>
    <h2>营销中心</h2>
    <div class="card" style="margin-top:16px">
      <p>教师主页：<router-link :to="`/teachers/${marketing.slug}`">/teachers/{{ marketing.slug }}</router-link></p>
      <el-button type="primary" style="margin-top:12px" @click="createLink">生成推广链接</el-button>
      <el-table :data="marketing.links || []" style="margin-top:16px">
        <el-table-column prop="code" label="推广码" />
        <el-table-column prop="url" label="链接" />
        <el-table-column prop="click_count" label="点击" width="80" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../api/request'
const marketing = ref({ links: [] })
const load = async () => { marketing.value = (await request.get('/teacher/marketing')).data }
const createLink = async () => {
  await request.post('/teacher/marketing/links', {})
  ElMessage.success('推广链接已生成')
  load()
}
onMounted(load)
</script>
