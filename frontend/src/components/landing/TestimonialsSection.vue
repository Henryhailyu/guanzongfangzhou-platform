<template>
  <section class="landing-section section-light">
    <div class="landing-container">
      <div class="section-heading">
        <h2>来自学员与老师的真实期待</h2>
      </div>
      <div class="grid-2">
        <div v-for="(t, i) in testimonials" :key="i" class="testimonial feature-card">
          <div class="type">{{ t.type === 'student' ? '学员' : '老师' }}</div>
          <p class="quote">"{{ t.content }}"</p>
          <div class="author">— {{ t.author }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { testimonials } from '../../data/landing.mock.js'
</script>

<style scoped>
.type { font-size: 12px; color: var(--color-primary); font-weight: 600; margin-bottom: 12px; }
.quote { font-size: 15px; line-height: 1.8; color: #374151; margin: 0 0 16px; }
.author { font-size: 14px; color: #9ca3af; }
</style>
