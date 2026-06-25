<template>
  <div v-if="data">
    <h2>{{ data.teacher.nickname }} 的老师主页</h2>
    <div class="grid">
      <div v-for="c in data.courses" :key="c.id" class="card" @click="$router.push(`/courses/${c.id}`)">
        <h3>{{ c.title }}</h3>
        <p>¥{{ c.price }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import request from '../../api/request'
const route = useRoute()
const data = ref(null)
onMounted(async () => {
  data.value = (await request.get(`/teachers/${route.params.slug}`)).data
})
</script>

<style scoped>
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; margin-top: 24px; }
.card { cursor: pointer; }
</style>
