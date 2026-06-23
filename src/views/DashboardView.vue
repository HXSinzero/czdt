<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function restart() {
  router.push('/')
}
</script>

<template>
  <section class="interaction-screen flow-screen">
    <div class="flow-header">
      <span>Dashboard</span>
      <strong>数据展示页</strong>
    </div>

    <div class="display-stack" aria-label="数据展示占位">
      <div class="display-hero"></div>
      <div class="display-row" v-for="index in 3" :key="index"></div>
    </div>

    <button class="bottom-action" type="button" @click="restart">重新开始</button>
  </section>
</template>

<style scoped>
.display-stack {
  display: grid;
  align-content: start;
  gap: 14px;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  overscroll-behavior: contain;
  scrollbar-width: none;
}

.display-stack::-webkit-scrollbar {
  display: none;
}

.display-hero,
.display-row {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #ffffff;
}

.display-hero {
  min-height: 180px;
}

.display-row {
  min-height: 74px;
}
</style>
