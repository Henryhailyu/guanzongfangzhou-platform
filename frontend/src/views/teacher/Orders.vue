<template>
  <div>
    <h2>收入与订单</h2>
    <p class="desc">以下为购买您课程的用户订单（已支付订单计入收入分成）</p>
    <el-table :data="orders" empty-text="暂无订单" style="margin-top:16px">
      <el-table-column prop="order_no" label="订单号" min-width="140" />
      <el-table-column prop="user_nickname" label="学员" width="120" />
      <el-table-column prop="product_title" label="课程" />
      <el-table-column prop="amount" label="订单金额" width="100">
        <template #default="{ row }">¥{{ row.amount }}</template>
      </el-table-column>
      <el-table-column prop="teacher_income" label="您的收入" width="100">
        <template #default="{ row }">
          <span v-if="row.status === 'paid'">¥{{ row.teacher_income }}</span>
          <span v-else>—</span>
        </template>
      </el-table-column>
      <el-table-column prop="status_label" label="状态" width="100" />
      <el-table-column prop="paid_at" label="支付时间" width="180">
        <template #default="{ row }">{{ formatTime(row.paid_at || row.created_at) }}</template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../../api/request'

const orders = ref([])
const formatTime = (t) => (t ? new Date(t).toLocaleString('zh-CN') : '—')

onMounted(async () => {
  orders.value = (await request.get('/teacher/orders')).data
})
</script>

<style scoped>
.desc { color: var(--color-text-muted); font-size: 14px; margin-top: -8px; }
</style>
