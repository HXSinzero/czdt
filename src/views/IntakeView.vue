<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goNext() {
  router.push('/dashboard')
}
</script>

<template>
  <section class="interaction-screen flow-screen">
    <div class="flow-header">
      <span>Intake</span>
      <strong>信息收集页</strong>
    </div>

    <div class="input-stack" aria-label="信息收集占位">
      <label v-for="index in 4" :key="index" class="input-tile">
        <span>信息项 {{ index }}</span>
        <input type="text" />
      </label>
    </div>

    <button class="bottom-action" type="button" @click="goNext">查看结果</button>
  </section>
</template>

<style scoped>
.input-stack {
  display: grid;
  align-content: start;
  gap: 14px;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  overscroll-behavior: contain;
  scrollbar-width: none;
}

.input-stack::-webkit-scrollbar {
  display: none;
}

.input-tile {
  display: grid;
  gap: 8px;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #ffffff;
}

.input-tile span {
  color: #405066;
  font-weight: 800;
}

.input-tile input {
  height: 42px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #f8fafc;
}
</style>
