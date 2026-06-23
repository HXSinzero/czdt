<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const title = computed(() => route.meta.pageTitle || '职页成长指引')
const subtitle = computed(() => route.meta.subtitle || '')
const showBack = computed(() => route.name !== 'home')
const rightLabel = computed(() => route.meta.rightLabel || '')

function goBack() {
  if (route.name === 'home') return
  router.push('/')
}
</script>

<template>
  <main class="app-shell">
    <header class="app-topbar">
      <button class="nav-orb" type="button" :aria-label="showBack ? '返回' : '首页'" @click="goBack">
        <span v-if="showBack" class="back-mark"></span>
        <span v-else class="home-mark">职</span>
      </button>

      <div class="app-title">
        <div class="title-divider" aria-hidden="true"></div>
        <h1>{{ title }}</h1>
        <p v-if="subtitle">{{ subtitle }}</p>
      </div>

      <button class="overview-orb" type="button" :aria-label="rightLabel || '总览'">
        <span></span>
        <b>{{ rightLabel || '总览' }}</b>
      </button>
    </header>

    <section class="view-host">
      <slot></slot>
    </section>
  </main>
</template>

<style scoped>
.app-shell {
  position: relative;
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  width: min(100%, 430px);
  height: 100%;
  overflow: hidden;
  margin: 0 auto;
  color: #f8ecd5;
  background:
    radial-gradient(circle at 50% 42%, rgba(164, 188, 199, 0.3), transparent 38%),
    radial-gradient(circle at 50% 100%, rgba(104, 131, 146, 0.5), transparent 34%),
    linear-gradient(180deg, #111d2a 0%, #223545 54%, #102032 100%);
}

.app-shell::before {
  position: absolute;
  inset: 0;
  pointer-events: none;
  content: "";
  background:
    linear-gradient(90deg, rgba(255, 223, 159, 0.08), transparent 16%, transparent 84%, rgba(255, 223, 159, 0.08)),
    radial-gradient(circle at 50% 8%, rgba(255, 233, 184, 0.08), transparent 22%);
}

.app-topbar {
  position: relative;
  z-index: 20;
  display: grid;
  grid-template-columns: 56px 1fr 56px;
  align-items: center;
  gap: 10px;
  min-height: 90px;
  padding: 18px 16px 8px;
  background: transparent;
  pointer-events: none;
}

.app-topbar button {
  pointer-events: auto;
}

.nav-orb,
.overview-orb {
  display: grid;
  place-items: center;
  width: 54px;
  min-width: 0;
  height: 54px;
  padding: 0;
  border: 1px solid rgba(246, 216, 153, 0.72);
  border-radius: 50%;
  color: #f9e9c9;
  background:
    radial-gradient(circle, rgba(255, 239, 204, 0.18), transparent 58%),
    rgba(12, 21, 31, 0.28);
  box-shadow:
    0 0 18px rgba(244, 196, 101, 0.42),
    inset 0 0 12px rgba(255, 244, 204, 0.16);
}

.back-mark {
  width: 18px;
  height: 18px;
  border-bottom: 4px solid currentColor;
  border-left: 4px solid currentColor;
  transform: translateX(4px) rotate(45deg);
}

.home-mark {
  font-weight: 900;
}

.overview-orb {
  grid-template-rows: 28px auto;
  gap: 1px;
  font-size: 12px;
  font-weight: 900;
}

.overview-orb span {
  position: relative;
  width: 24px;
  height: 20px;
  border: 2px solid currentColor;
  border-radius: 3px 3px 7px 7px;
}

.overview-orb span::before {
  position: absolute;
  top: 3px;
  left: 50%;
  width: 1px;
  height: 12px;
  background: currentColor;
  content: "";
}

.overview-orb b {
  font-weight: 900;
}

.app-title {
  display: grid;
  justify-items: center;
  gap: 2px;
  min-width: 0;
  text-align: center;
}

.app-title h1 {
  margin: 0;
  color: #fff6e6;
  font-family: "STKaiti", "KaiTi", "Songti SC", serif;
  font-size: 36px;
  line-height: 1;
  letter-spacing: 0;
  text-shadow:
    0 2px 0 rgba(64, 42, 22, 0.28),
    0 0 14px rgba(255, 231, 176, 0.22);
}

.app-title p {
  margin: 0;
  color: #f7e7c8;
  font-family: "STKaiti", "KaiTi", "Songti SC", serif;
  font-size: 17px;
  font-weight: 700;
}

.title-divider {
  position: relative;
  width: min(100%, 210px);
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(247, 222, 166, 0.66), transparent);
}

.title-divider::before,
.title-divider::after {
  position: absolute;
  top: -3px;
  width: 7px;
  height: 7px;
  border: 1px solid rgba(247, 222, 166, 0.78);
  content: "";
  transform: rotate(45deg);
}

.title-divider::before {
  left: 24px;
}

.title-divider::after {
  right: 24px;
}

.view-host {
  position: relative;
  z-index: 1;
  min-height: 0;
  overflow: hidden;
}

@media (max-height: 760px) {
  .app-topbar {
    grid-template-columns: 48px 1fr 48px;
    min-height: 74px;
    padding-top: 12px;
  }

  .nav-orb,
  .overview-orb {
    width: 46px;
    height: 46px;
  }

  .app-title h1 {
    font-size: 30px;
  }

  .app-title p {
    font-size: 15px;
  }
}
</style>
