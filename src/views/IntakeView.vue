<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPublicAssetUrl } from '../config'

const route = useRoute()
const router = useRouter()
const growthTree = ref([])
const levelList = ref([])
const loading = ref(true)
const loadError = ref('')
const isRelatedMajor = ref(true)
const screenRef = ref(null)
const scrollingTitleKeys = ref(new Set())
const sceneImage = `url("${getPublicAssetUrl('contents/directions.webp')}")`

const selectedDirectionName = computed(() => String(route.query.direction || '').trim())
const selectedDirection = computed(() => {
  if (!selectedDirectionName.value) return null
  return growthTree.value.find((item) => item.name === selectedDirectionName.value) || null
})
const rawQualifications = computed(() => selectedDirection.value?.children || [])
const hasMajorFilter = computed(() => rawQualifications.value.some((item) => item.root === false))
const qualifications = computed(() => rawQualifications.value
  .map((qualification, index) => ({
    ...attachLevelMeta(resolveQualification(qualification)),
    sourceIndex: index
  }))
  .sort((current, next) => {
    const currentLevel = Number(current.level)
    const nextLevel = Number(next.level)

    if (Number.isFinite(currentLevel) && Number.isFinite(nextLevel)) return currentLevel - nextLevel
    if (Number.isFinite(currentLevel)) return -1
    if (Number.isFinite(nextLevel)) return 1
    return current.sourceIndex - next.sourceIndex
  }))

onMounted(async () => {
  try {
    const [dataResponse, levelResponse] = await Promise.all([
      fetch(getPublicAssetUrl('contents/data.json')),
      fetch(getPublicAssetUrl('contents/level.json'))
    ])

    if (!dataResponse.ok) throw new Error(`HTTP ${dataResponse.status}`)
    growthTree.value = await dataResponse.json()

    if (levelResponse.ok) {
      levelList.value = await levelResponse.json()
    }
  } catch (error) {
    loadError.value = '资料暂未载入'
  } finally {
    loading.value = false
    scheduleTitleMeasure()
  }

  window.addEventListener('resize', scheduleTitleMeasure)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', scheduleTitleMeasure)
})

watch(qualifications, scheduleTitleMeasure, { flush: 'post' })

function getQualificationIntro(qualification) {
  if (qualification.description) return qualification.description

  const children = qualification.children || []
  if (!children.length) return '暂未收录可行路径，稍后补全。'

  const years = children
    .map((child) => child.year)
    .filter((year) => Number.isFinite(Number(year)))
    .map(Number)

  const minYear = years.length ? Math.min(...years) : 0
  const targetNames = children.slice(0, 2).map((child) => child.name).join('、')
  const suffix = children.length > 2 ? '等路径' : '路径'

  return `${targetNames}${suffix}，${minYear || 1}年起步。`
}

function resolveQualification(qualification) {
  if (qualification.root !== false) return qualification

  const targetName = isRelatedMajor.value ? '相关专业' : '非相关专业'
  const fallbackName = isRelatedMajor.value ? '非相关专业' : '相关专业'
  const children = qualification.children || []
  const matched = children.find((child) => child.name === targetName)
    || children.find((child) => child.name === fallbackName)
    || children[0]

  if (!matched) return qualification

  return {
    ...qualification,
    children: matched.children || [],
    major: matched.name,
    root: matched.root
  }
}

function getSpeedLabel(qualification, index) {
  const children = qualification.children || []
  const years = children.map((child) => Number(child.year || 0)).filter(Boolean)
  const minYear = years.length ? Math.min(...years) : index + 1
  const score = Math.max(0, 60 - minYear * 5)

  return `适配度 +${score}%`
}

function getLevelMeta(qualification) {
  const target = String(qualification.name || '').trim()

  return levelList.value.find((item) => {
    const keys = String(item.keys || '')
      .split(';')
      .map((key) => key.trim())
      .filter(Boolean)

    return keys.some((key) => target.includes(key))
  })
}

function attachLevelMeta(qualification) {
  const level = getLevelMeta(qualification)
  if (!level) return qualification

  return {
    ...qualification,
    level: level.level,
    levelName: level.name || '',
    description: level.description || '',
    levelPic: level.pic || ''
  }
}

function getLevelPic(qualification) {
  return qualification.levelPic ? `url("${getPublicAssetUrl(qualification.levelPic, 'contents')}")` : sceneImage
}

function getTitleKey(qualification) {
  return `${qualification.sourceIndex}-${qualification.name}-${qualification.levelName || ''}-${qualification.major || ''}`
}

function shouldScrollTitle(qualification) {
  return scrollingTitleKeys.value.has(getTitleKey(qualification))
}

async function scheduleTitleMeasure() {
  await nextTick()
  measureTitleOverflow()
}

function measureTitleOverflow() {
  const root = screenRef.value
  if (!root) return

  const nextKeys = new Set()
  root.querySelectorAll('[data-title-key]').forEach((title) => {
    const key = title.getAttribute('data-title-key')
    if (key && title.scrollWidth > title.clientWidth + 1) {
      nextKeys.add(key)
    }
  })

  scrollingTitleKeys.value = nextKeys
}

function selectQualification(qualification) {
  router.push({
    path: '/dashboard',
    query: {
      direction: selectedDirectionName.value,
      qualification: qualification.name,
      major: qualification.major || ''
    }
  })
}
</script>

<template>
  <section ref="screenRef" class="interaction-screen qualification-screen">
    <div v-if="loading" class="qualification-state">正在翻阅卷宗...</div>
    <div v-else-if="loadError" class="qualification-state">{{ loadError }}</div>
    <div v-else-if="!selectedDirection" class="qualification-state">未找到对应方向</div>

    <div v-else class="qualification-content">
      <label v-if="hasMajorFilter" class="major-filter">
        <input v-model="isRelatedMajor" type="checkbox" />
        <span>相关专业</span>
      </label>

      <div class="qualification-list" aria-label="学历选择">
      <button
        v-for="(qualification, index) in qualifications"
        :key="qualification.name"
        type="button"
        class="qualification-card"
        :class="{ featured: index === 0 }"
        :style="{ '--scene-image': getLevelPic(qualification) }"
        @click="selectQualification(qualification)"
      >
        <div class="qualification-card__body">
          <h2
            :class="{ scrolling: shouldScrollTitle(qualification) }"
            :data-title-key="getTitleKey(qualification)"
          >
            <span>{{ qualification.levelName || qualification.name }}</span>
          </h2>
          <small v-if="qualification.major">{{ qualification.major }}</small>
          <p>{{ getQualificationIntro(qualification) }}</p>
        </div>
      </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.qualification-screen {
  position: relative;
  height: 100%;
  padding: 52px 20px 22px;
  overflow: hidden;
  color: var(--ink);
}

.qualification-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  gap: 14px;
  height: 100%;
  min-height: 0;
}

.major-filter {
  display: inline-grid;
  grid-template-columns: 24px auto;
  align-items: center;
  justify-self: start;
  gap: 8px;
  min-height: 36px;
  padding: 0 14px;
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  color: var(--ink);
  background: rgba(246, 250, 244, 0.68);
  box-shadow:
    inset 0 0 12px rgba(255, 255, 255, 0.52),
    0 0 14px rgba(91, 131, 118, 0.16);
  font-family: var(--app-font);
  font-size: 18px;
  font-weight: 900;
}

.major-filter input {
  width: 18px;
  height: 18px;
  margin: 0;
  accent-color: var(--jade);
}

.qualification-list {
  display: grid;
  gap: 14px;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0 2px 12px;
  overscroll-behavior: contain;
  scrollbar-width: none;
}

.qualification-list::-webkit-scrollbar {
  display: none;
}

.qualification-card {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  min-height: 132px;
  padding: 0;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
  color: inherit;
  background:
    linear-gradient(90deg, rgba(246, 250, 244, 0) 0%, rgba(246, 250, 244, 0.18) 32%, rgba(238, 247, 241, 0.72) 56%, rgba(230, 242, 235, 0.94) 76%),
    var(--scene-image) center / 100% 100% no-repeat,
    var(--paper-soft);
  box-shadow:
    inset 0 0 20px rgba(255, 255, 255, 0.38),
    0 10px 24px var(--shadow-soft);
  text-align: left;
  touch-action: manipulation;
  transition:
    transform 160ms ease,
    border-color 160ms ease,
    box-shadow 160ms ease,
    filter 160ms ease;
}

.qualification-card:active {
  border-color: rgba(91, 131, 118, 0.86);
  box-shadow:
    inset 0 0 24px rgba(255, 255, 255, 0.46),
    0 4px 12px rgba(43, 83, 72, 0.2);
  filter: saturate(1.05) brightness(0.98);
  transform: scale(0.985);
}

.qualification-card.featured {
  border-color: rgba(91, 131, 118, 0.72);
  box-shadow:
    0 0 0 1px rgba(246, 250, 244, 0.72),
    0 0 22px rgba(101, 157, 139, 0.36),
    inset 0 0 18px rgba(255, 255, 255, 0.26);
}

.qualification-card__body {
  display: grid;
  align-content: center;
  justify-self: end;
  width: 58%;
  min-width: 0;
  padding: 16px 18px 54px;
}

.qualification-card h2 {
  width: 100%;
  min-width: 0;
  overflow: hidden;
  margin: 0;
  color: var(--ink);
  font-family: var(--app-font);
  font-size: 32px;
  line-height: 1;
  letter-spacing: 0;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.55);
  white-space: nowrap;
}

.qualification-card h2 span {
  display: inline-block;
  min-width: 100%;
}

.qualification-card h2.scrolling span {
  animation: titleMarquee 7.2s linear infinite;
}

.qualification-card small {
  margin-top: 4px;
  color: var(--green);
  font-size: 13px;
  font-weight: 900;
  line-height: 1;
}

.qualification-card p {
  margin: 10px 0 0;
  color: var(--ink-soft);
  font-size: 17px;
  line-height: 1.6;
  white-space: pre-line;
}

.qualification-card strong {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  color: var(--green);
  font-size: 14px;
  line-height: 1;
}

.qualification-card strong span {
  display: grid;
  width: 20px;
  height: 20px;
  place-items: center;
  border-radius: 50%;
  color: var(--paper);
  background: rgba(95, 157, 140, 0.86);
  font-size: 12px;
}

.qualification-state {
  display: grid;
  height: 100%;
  place-items: center;
  color: var(--ink);
  font-family: var(--app-font);
  font-size: 24px;
}

@keyframes titleMarquee {
  0%,
  18% {
    transform: translateX(0);
  }

  56%,
  74% {
    transform: translateX(-42%);
  }

  74.1%,
  100% {
    transform: translateX(0);
  }
}

@media (max-height: 760px) {
  .qualification-screen {
    padding-top: 34px;
  }

  .qualification-content,
  .qualification-list {
    gap: 10px;
  }

  .major-filter {
    min-height: 32px;
    font-size: 16px;
  }

  .qualification-card {
    min-height: 112px;
  }

  .qualification-card__body {
    width: 60%;
    padding: 12px 14px 46px;
  }

  .qualification-card h2 {
    font-size: 27px;
  }

  .qualification-card p,
  .qualification-card strong {
    font-size: 14px;
  }

}
</style>
