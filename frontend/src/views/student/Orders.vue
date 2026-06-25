<template>
  <div>
    <h2>我的订单</h2>
    <el-tabs v-model="status" @tab-change="load">
      <el-tab-pane label="全部" name="" />
      <el-tab-pane label="待支付" name="pending" />
      <el-tab-pane label="已完成" name="paid" />
    </el-tabs>

    <el-table :data="orders" empty-text="暂无订单" style="margin-top:16px">
      <el-table-column prop="order_no" label="订单号" min-width="160">
        <template #default="{ row }">
          <router-link :to="`/orders/${row.id}`" class="order-link">{{ row.order_no.slice(0, 12) }}…</router-link>
        </template>
      </el-table-column>
      <el-table-column prop="product_title" label="商品" />
      <el-table-column prop="amount" label="金额" width="90">
        <template #default="{ row }">¥{{ row.amount }}</template>
      </el-table-column>
      <el-table-column prop="status_label" label="状态" width="100" />
      <el-table-column prop="created_at" label="下单时间" width="180">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" size="small" type="primary" @click="pay(row)">去支付</el-button>
          <el-button v-if="row.status === 'pending'" size="small" link @click="cancel(row.id)">取消</el-button>
          <router-link v-if="row.status === 'paid' && row.product_type === 'course'" :to="`/courses/${row.product_id}`">
            <el-button size="small" link>去学习</el-button>
          </router-link>
        </template>
      </el-table-column>
    </el-table>

    <CheckoutDialog
      :visible="checkoutVisible"
      :order-id="checkout.orderId"
      :product-type="checkout.productType"
      :product-id="checkout.productId"
      :product-title="checkout.productTitle"
      :amount="checkout.amount"
      :points-granted="checkout.pointsGranted"
      title="继续支付"
      @close="checkoutVisible = false"
      @success="onPaid"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../api/request'
import CheckoutDialog from '../../components/CheckoutDialog.vue'

const orders = ref([])
const status = ref('')
const checkoutVisible = ref(false)
const checkout = ref({ orderId: null, productType: '', productId: null, productTitle: '', amount: 0, pointsGranted: 0 })

const formatTime = (t) => (t ? new Date(t).toLocaleString('zh-CN') : '—')

const load = async () => {
  const params = status.value ? { status: status.value } : {}
  orders.value = (await request.get('/orders', { params })).data
}

const pay = (row) => {
  checkout.value = {
    orderId: row.id,
    productType: row.product_type,
    productId: row.product_id,
    productTitle: row.product_title,
    amount: row.amount,
    pointsGranted: row.points_granted,
  }
  checkoutVisible.value = true
}

const cancel = async (id) => {
  await ElMessageBox.confirm('确定取消该订单？', '提示', { type: 'warning' })
  await request.post(`/orders/${id}/cancel`)
  ElMessage.success('订单已取消')
  load()
}

const onPaid = () => load()

onMounted(load)
</script>

<style scoped>
.order-link { color: var(--color-primary); font-size: 13px; }
</style>
