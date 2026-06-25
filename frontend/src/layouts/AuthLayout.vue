<template>
  <div class="auth-layout">
    <router-link to="/" class="auth-brand">
      <span class="icon">⛵</span>
      <div>
        <div class="name">On-Board 管综方舟</div>
        <div class="sub">你的管理类联考上岸驾驶舱</div>
      </div>
    </router-link>
    <main class="auth-main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  background: linear-gradient(160deg, #f0f4ff 0%, #f7f8fa 50%, #eef2ff 100%);
  padding: 32px 16px 64px;
}
.auth-brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #1a1a2e;
  margin-bottom: 32px;
}
.icon { font-size: 28px; }
.name { font-weight: 700; font-size: 18px; }
.sub { font-size: 12px; color: #6b7280; margin-top: 2px; }
.auth-main { display: flex; justify-content: center; }
</style>
