<template>
  <section class="hero">
    <div class="hero-bg" :style="{ backgroundImage: `url(${heroBg})` }"></div>
    <div class="hero-overlay"></div>
    <div class="landing-container hero-grid">
      <div class="hero-content fade-in-up">
        <div class="hero-badge">你的管理类联考上岸驾驶舱</div>
        <h1>
          管理类联考，不只是刷题。<br />
          <span class="gold">On-Board 管综方舟</span>，带你系统上岸。
        </h1>
        <p class="hero-desc">
          覆盖数学、逻辑、写作与英语二，融合智能题库、AI 批改、学习路径、名师课程与数据化督学，
          为 MBA / MPA / MPAcc / MEM / MAud 考生打造一站式备考驾驶舱。
        </p>
        <div class="hero-tags">
          <span v-for="tag in heroTags" :key="tag.text" class="tag">{{ tag.icon }} {{ tag.text }}</span>
        </div>
        <div class="hero-actions">
          <router-link to="/register/student" class="landing-btn-primary">开始我的上岸计划 →</router-link>
          <router-link to="/register/teacher" class="landing-btn-outline">申请成为入驻老师 →</router-link>
        </div>
      </div>

      <div class="cockpit float-animation">
        <div class="glass-card cockpit-card">
          <div class="cockpit-header">
            <span>🧭</span> 上岸驾驶舱
          </div>
          <div class="cockpit-body">
            <div class="progress-ring">
              <svg viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="10"/>
                <circle cx="60" cy="60" r="52" fill="none" stroke="#22d3ee" stroke-width="10"
                  stroke-dasharray="326.7" :stroke-dashoffset="326.7 * (1 - 0.67)" stroke-linecap="round"
                  transform="rotate(-90 60 60)"/>
              </svg>
              <div class="progress-text">
                <strong>67%</strong>
                <small>上岸进度</small>
              </div>
            </div>
            <div class="tasks">
              <div class="tasks-title">今日任务</div>
              <div v-for="t in heroTasks" :key="t.name" class="task-item" :class="{ done: t.done }">
                <span class="check">{{ t.done ? '✓' : '○' }}</span> {{ t.name }}
              </div>
            </div>
          </div>
          <div class="subjects-row">
            <span v-for="s in ['数学','逻辑','写作','英语二']" :key="s" class="subj">{{ s }}</span>
          </div>
          <div class="ai-tip">
            <span>🤖</span>
            <div>
              <strong>AI 助教提示</strong>
              <p>你本周逻辑论证题正确率提升 18%</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { heroTags, heroTasks } from '../../data/landing.mock.js'
const heroBg = '/images/landing/hero-bg.png'
</script>

<style scoped>
.hero {
  position: relative; min-height: 100vh; display: flex; align-items: center;
  padding: 120px 0 80px; overflow: hidden;
}
.hero-bg {
  position: absolute; inset: 0; background-size: cover; background-position: center 30%;
}
.hero-overlay {
  position: absolute; inset: 0;
  background:
    linear-gradient(105deg, rgba(10, 22, 40, 0.88) 0%, rgba(10, 22, 40, 0.72) 42%, rgba(10, 22, 40, 0.45) 100%),
    linear-gradient(180deg, rgba(10, 22, 40, 0.3) 0%, transparent 40%);
}
.hero-grid {
  position: relative; z-index: 1;
  display: grid; grid-template-columns: 1fr 420px; gap: 48px; align-items: center;
}
.hero-badge {
  display: inline-block; padding: 6px 14px; border-radius: 20px;
  background: rgba(34,211,238,0.15); color: #22d3ee; font-size: 13px; margin-bottom: 20px;
}
h1 { font-size: clamp(32px, 4.5vw, 48px); font-weight: 700; line-height: 1.25; margin: 0 0 20px; }
.gold { color: #e8c468; }
.hero-desc { font-size: 16px; color: rgba(255,255,255,0.78); line-height: 1.8; margin: 0 0 24px; max-width: 560px; }
.hero-tags { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 32px; }
.tag {
  font-size: 12px; padding: 8px 14px; border-radius: 8px;
  background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
}
.hero-actions { display: flex; flex-wrap: wrap; gap: 16px; }
.cockpit-card { padding: 20px; }
.cockpit-header { font-weight: 600; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.cockpit-body { display: flex; gap: 20px; margin-bottom: 16px; }
.progress-ring { position: relative; width: 100px; height: 100px; flex-shrink: 0; }
.progress-ring svg { width: 100%; height: 100%; }
.progress-text { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.progress-text strong { font-size: 22px; color: #22d3ee; }
.progress-text small { font-size: 11px; color: rgba(255,255,255,0.6); }
.tasks { flex: 1; }
.tasks-title { font-size: 13px; color: rgba(255,255,255,0.6); margin-bottom: 8px; }
.task-item { font-size: 13px; padding: 4px 0; color: rgba(255,255,255,0.85); }
.task-item.done { color: #22d3ee; }
.check { margin-right: 6px; }
.subjects-row { display: flex; gap: 8px; margin-bottom: 12px; }
.subj {
  flex: 1; text-align: center; font-size: 11px; padding: 8px 4px; border-radius: 8px;
  background: rgba(255,255,255,0.06);
}
.ai-tip {
  display: flex; gap: 12px; padding: 12px; border-radius: 10px;
  background: rgba(34,211,238,0.1); border: 1px solid rgba(34,211,238,0.2);
}
.ai-tip strong { font-size: 13px; display: block; }
.ai-tip p { font-size: 12px; margin: 4px 0 0; color: rgba(255,255,255,0.75); }

@media (max-width: 1024px) {
  .hero-grid { grid-template-columns: 1fr; }
  .cockpit { max-width: 420px; margin: 0 auto; }
}
@media (max-width: 768px) {
  .hero { padding-top: 100px; min-height: auto; }
  .hero-actions { flex-direction: column; }
  .hero-actions a { text-align: center; justify-content: center; }
}
</style>
