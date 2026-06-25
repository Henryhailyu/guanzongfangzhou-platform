<template>
  <div>
    <div class="header-row">
      <h2>错题本</h2>
      <el-select v-model="subject" placeholder="全部科目" clearable style="width:140px" @change="load">
        <el-option label="数学" value="math" />
        <el-option label="逻辑" value="logic" />
      </el-select>
    </div>
    <el-table :data="items" style="width:100%;margin-top:16px" empty-text="暂无错题，继续保持！">
      <el-table-column prop="subject_label" label="科目" width="80" />
      <el-table-column prop="tag" label="知识点" width="100" />
      <el-table-column prop="stem" label="题目" min-width="280" show-overflow-tooltip />
      <el-table-column prop="wrong_count" label="错误次数" width="100" align="center" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <router-link :to="`/practice?q=${row.question_id}`">
            <el-button size="small" type="primary" link>再练一次</el-button>
          </router-link>
          <el-button size="small" @click="master(row.id)">已掌握</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../api/request'

const items = ref([])
const subject = ref('')

const load = async () => {
  items.value = (await request.get('/wrong-book', {
    params: subject.value ? { subject: subject.value } : {},
  })).data
}

const master = async (id) => {
  await request.delete(`/wrong-book/${id}`)
  ElMessage.success('已标记掌握')
  load()
}

onMounted(load)
</script>

<style scoped>
.header-row { display: flex; justify-content: space-between; align-items: center; }
</style>
