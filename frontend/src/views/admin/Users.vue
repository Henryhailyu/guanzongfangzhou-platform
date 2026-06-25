<template>
  <div>
    <h2>用户管理</h2>
    <el-table :data="users" style="margin-top:16px">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="role" label="角色" width="100" />
      <el-table-column prop="points" label="积分" width="80" />
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../../api/request'
const users = ref([])
onMounted(async () => { users.value = (await request.get('/admin/users')).data })
</script>
