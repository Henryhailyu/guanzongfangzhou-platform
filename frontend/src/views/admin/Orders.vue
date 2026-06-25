<template>
  <div>
    <h2>订单管理</h2>
    <el-table :data="orders" empty-text="暂无订单" style="margin-top:16px">
      <el-table-column prop="order_no" label="订单号" min-width="140" />
      <el-table-column prop="user_nickname" label="用户" width="120" />
      <el-table-column prop="product_title" label="商品" min-width="140" />
      <el-table-column prop="product_type_label" label="类型" width="90" />
      <el-table-column prop="amount" label="金额" width="90">
        <template #default="{ row }">¥{{ row.amount }}</template>
      </el-table-column>
      <el-table-column prop="payment_method_label" label="支付方式" width="110" />
      <el-table-column prop="status_label" label="状态" width="100" />
      <el-table-column prop="created_at" label="下单时间" width="180">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
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
  orders.value = (await request.get('/admin/orders')).data
})
</script>
