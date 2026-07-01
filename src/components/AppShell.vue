<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPublicAssetUrl } from '../config'

const route = useRoute()
const router = useRouter()

const title = computed(() => route.meta.pageTitle || '职页成长指引')
const subtitle = computed(() => route.meta.subtitle || '')
const showBack = computed(() => route.name !== 'home')
const rightLabel = computed(() => route.meta.rightLabel || '')
const shellStyle = computed(() => ({
  '--main-bg': `url("${getPublicAssetUrl('contents/MainBG.webp')}")`
}))

function goBack() {
  if (route.name === 'home') return
  if (window.history.length > 1) {
    router.back()
    return
  }

  router.push('/')
}

function goHome() {
  router.push('/')
}
</script>

<template>
  <main class="app-shell" :style="shellStyle">
    <header class="app-topbar">
      <button class="nav-orb" type="button" :aria-label="showBack ? '返回' : '首页'" @click.stop="goBack">
        <span v-if="showBack" class="back-mark"></span>
        <span v-else class="home-mark">职</span>
      </button>

      <div class="app-title">
        <div class="title-divider" aria-hidden="true"></div>
        <h1>{{ title }}</h1>
        <p v-if="subtitle">{{ subtitle }}</p>
      </div>

      <button class="overview-orb" type="button" :aria-label="rightLabel || '总览'" @click.stop="goHome">
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
  color: var(--ink);
  background:
    linear-gradient(180deg, rgba(248, 252, 246, 0.24), rgba(229, 241, 235, 0.22)),
    var(--main-bg) center / cover no-repeat,
    linear-gradient(180deg, #eef6f1 0%, #dceee6 52%, #c6dfd5 100%);
}

.app-shell::before {
  position: absolute;
  inset: 0;
  pointer-events: none;
  content: "";
  background:
    linear-gradient(180deg, rgba(248, 252, 246, 0.18), transparent 26%, rgba(229, 241, 235, 0.12)),
    linear-gradient(90deg, rgba(82, 128, 115, 0.08), transparent 18%, transparent 82%, rgba(82, 128, 115, 0.08));
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
  user-select: none;
  -webkit-user-select: none;
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
  border: 1px solid rgba(91, 131, 118, 0.5);
  border-radius: 50%;
  color: var(--ink);
  background:
    radial-gradient(circle, rgba(255, 255, 255, 0.7), transparent 62%),
    rgba(237, 247, 240, 0.46);
  box-shadow:
    0 0 18px rgba(87, 134, 119, 0.22),
    inset 0 0 12px rgba(255, 255, 255, 0.58);
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
  color: var(--ink);
  font-family: var(--app-font);
  font-size: 36px;
  line-height: 1;
  letter-spacing: 0;
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.64),
    0 0 14px rgba(100, 145, 130, 0.16);
}

.app-title p {
  margin: 0;
  color: var(--ink-soft);
  font-family: var(--app-font);
  font-size: 17px;
  font-weight: 700;
}

.title-divider {
  position: relative;
  width: min(100%, 210px);
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(91, 131, 118, 0.54), transparent);
}

.title-divider::before,
.title-divider::after {
  position: absolute;
  top: -3px;
  width: 7px;
  height: 7px;
  border: 1px solid rgba(91, 131, 118, 0.62);
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
