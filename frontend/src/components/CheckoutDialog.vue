<template>
  <el-dialog
    :model-value="visible"
    :title="title"
    width="440px"
    @close="$emit('close')"
  >
    <div v-if="productTitle" class="summary">
      <div class="product">{{ productTitle }}</div>
      <div class="amount">¥{{ amount }}</div>
      <p v-if="pointsGranted" class="bonus">支付成功赠送 {{ pointsGranted }} 积分</p>
    </div>

    <el-form label-width="80px">
      <el-form-item label="支付方式">
        <el-radio-group v-model="paymentMethod">
          <el-radio value="wechat">微信支付（模拟）</el-radio>
          <el-radio value="alipay">支付宝（模拟）</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>

    <el-alert
      type="info"
      :closable="false"
      show-icon
      title="开发环境模拟支付"
      description="正式环境将跳转微信/支付宝收银台，支付成功后自动开通权益。"
      style="margin-top: 8px"
    />

    <template #footer>
      <el-button @click="$emit('close')">取消</el-button>
      <el-button type="primary" :loading="loading" @click="submit">
        确认支付 ¥{{ amount }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../api/request'

const props = defineProps({
  visible: Boolean,
  orderId: { type: [Number, String], default: null },
  productType: { type: String, default: 'course' },
  productId: { type: [Number, String], default: null },
  productTitle: String,
  amount: { type: Number, default: 0 },
  pointsGranted: { type: Number, default: 0 },
  referralCode: String,
  title: { type: String, default: '确认订单' },
})

const emit = defineEmits(['close', 'success'])

const paymentMethod = ref('wechat')
const loading = ref(false)

watch(() => props.visible, (v) => {
  if (v) paymentMethod.value = 'wechat'
})

const submit = async () => {
  loading.value = true
  try {
    let orderId = props.orderId
    if (!orderId) {
      const payload = {
        product_type: props.productType,
        product_id: props.productId,
        payment_method: paymentMethod.value,
      }
      if (props.referralCode) payload.referral_code = props.referralCode
      const created = await request.post('/orders', payload)
      orderId = created.data.id
    }
    const paid = await request.post(`/orders/${orderId}/pay`, {
      payment_method: paymentMethod.value,
    })
    ElMessage.success('支付成功')
    emit('success', paid.data)
    emit('close')
  } catch (e) {
    ElMessage.error(e.message || '支付失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.summary { margin-bottom: 16px; padding: 16px; background: var(--color-surface); border-radius: 10px; }
.product { font-weight: 600; margin-bottom: 8px; }
.amount { font-size: 28px; font-weight: 700; color: var(--color-primary); }
.bonus { margin: 8px 0 0; font-size: 13px; color: var(--color-success); }
</style>
