<template>
  <section class="landing-section section-light">
    <div class="landing-container">
      <div class="section-heading">
        <h2>让学员更愿意报名，让老师更容易成交。</h2>
      </div>
      <div class="grid-3">
        <div v-for="m in marketingTools" :key="m.title" class="feature-card">
          <h3>{{ m.title }}</h3>
          <p>{{ m.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { marketingTools } from '../../data/landing.mock.js'
</script>
