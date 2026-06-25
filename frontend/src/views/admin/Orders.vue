<template>
  <div>
    <h2>订单管理</h2>
    <el-table :data="orders" style="margin-top:16px">
      <el-table-column prop="order_no" label="订单号" />
      <el-table-column prop="user_id" label="用户" width="80" />
      <el-table-column prop="amount" label="金额" width="100" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column prop="created_at" label="时间" />
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../../api/request'
const orders = ref([])
onMounted(async () => { orders.value = (await request.get('/admin/orders')).data })
</script>
