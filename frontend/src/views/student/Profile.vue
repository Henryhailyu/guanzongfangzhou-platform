<template>
  <div>
    <h2>个人中心</h2>
    <div class="card">
      <p>昵称：{{ auth.user?.nickname }}</p>
      <p>积分：{{ points }}</p>
      <p>角色：{{ auth.user?.role }}</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAuthStore } from '../../stores/auth'
import request from '../../api/request'
const auth = useAuthStore()
const points = ref(0)
onMounted(async () => { points.value = (await request.get('/points/balance')).data.points })
</script>
