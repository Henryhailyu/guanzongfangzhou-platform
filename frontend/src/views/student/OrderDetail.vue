<template>
  <div v-if="order">
    <router-link to="/orders" class="back">← 返回订单列表</router-link>
    <h2>订单详情</h2>

    <div class="card detail">
      <div class="row"><span>订单号</span><strong>{{ order.order_no }}</strong></div>
      <div class="row"><span>商品</span><strong>{{ order.product_title }}</strong></div>
      <div class="row"><span>类型</span><strong>{{ order.product_type_label }}</strong></div>
      <div class="row"><span>金额</span><strong class="price">¥{{ order.amount }}</strong></div>
      <div class="row"><span>状态</span><el-tag :type="statusType">{{ order.status_label }}</el-tag></div>
      <div class="row"><span>支付方式</span><strong>{{ order.payment_method_label || '—' }}</strong></div>
      <div v-if="order.points_granted" class="row"><span>赠送积分</span><strong>+{{ order.points_granted }}</strong></div>
      <div class="row"><span>下单时间</span><strong>{{ formatTime(order.created_at) }}</strong></div>
      <div v-if="order.paid_at" class="row"><span>支付时间</span><strong>{{ formatTime(order.paid_at) }}</strong></div>
    </div>

    <div v-if="order.status === 'pending'" class="actions">
      <el-button type="primary" @click="checkoutVisible = true">去支付</el-button>
      <el-button @click="cancel">取消订单</el-button>
    </div>

    <CheckoutDialog
      :visible="checkoutVisible"
      :order-id="order.id"
      :product-type="order.product_type"
      :product-id="order.product_id"
      :product-title="order.product_title"
      :amount="order.amount"
      :points-granted="order.points_granted"
      title="继续支付"
      @close="checkoutVisible = false"
      @success="reload"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../api/request'
import CheckoutDialog from '../../components/CheckoutDialog.vue'

const route = useRoute()
const router = useRouter()
const order = ref(null)
const checkoutVisible = ref(false)

const formatTime = (t) => (t ? new Date(t).toLocaleString('zh-CN') : '—')
const statusType = computed(() => ({ pending: 'warning', paid: 'success', cancelled: 'info' }[order.value?.status] || ''))

const load = async () => {
  order.value = (await request.get(`/orders/${route.params.id}`)).data
}

const reload = async () => {
  checkoutVisible.value = false
  await load()
}

const cancel = async () => {
  await ElMessageBox.confirm('确定取消该订单？', '提示', { type: 'warning' })
  await request.post(`/orders/${order.value.id}/cancel`)
  ElMessage.success('订单已取消')
  router.push('/orders')
}

onMounted(load)
</script>

<style scoped>
.back { display: inline-block; margin-bottom: 16px; font-size: 14px; color: var(--color-text-muted); }
.detail { padding: 24px; margin-top: 16px; }
.row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--color-border); }
.row:last-child { border-bottom: none; }
.row span { color: var(--color-text-muted); }
.price { color: var(--color-primary); font-size: 20px; }
.actions { margin-top: 20px; display: flex; gap: 12px; }
</style>
