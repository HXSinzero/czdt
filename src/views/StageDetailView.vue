<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getPublicAssetUrl } from '../config'

const route = useRoute()
const growthTree = ref([])
const loading = ref(true)
const loadError = ref('')
const fallbackImage = getPublicAssetUrl('contents/directions.webp')

const directionName = computed(() => String(route.query.direction || '').trim())
const qualificationName = computed(() => String(route.query.qualification || '').trim())
const majorName = computed(() => String(route.query.major || '').trim())
const stageName = computed(() => String(route.query.stage || '').trim())
const stageYear = computed(() => Number(route.query.year || 1))

const selectedDirection = computed(() => growthTree.value.find((item) => item.name === directionName.value) || null)
const selectedQualification = computed(() => {
  const qualification = selectedDirection.value?.children?.find((item) => item.name === qualificationName.value)
  if (!qualification) return null
  if (qualification.root !== false) return qualification

  const major = qualification.children?.find((item) => item.name === majorName.value)
    || qualification.children?.find((item) => item.name === '相关专业')
    || qualification.children?.[0]

  return major
    ? { ...qualification, children: major.children || [], major: major.name }
    : qualification
})
const stage = computed(() => {
  const stages = selectedQualification.value?.children || []
  return stages.find((item) => item.name === stageName.value && Number(item.year || 1) === stageYear.value)
    || stages.find((item) => item.name === stageName.value)
    || null
})
const detailText = computed(() => decodeBase64Text(stage.value?.txt).replace(/\s+/g, ' ').trim())
const storyText = computed(() => detailText.value || '此阶段资料正在补全，可先按照路径总览继续规划修行节奏。')
const shortIntro = computed(() => storyText.value.slice(0, 72))

onMounted(async () => {
  try {
    const response = await fetch(getPublicAssetUrl('contents/data.json'))
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    growthTree.value = await response.json()
  } catch (error) {
    loadError.value = '详情暂未载入'
  } finally {
    loading.value = false
  }
})

function decodeBase64Text(value) {
  if (!value) return ''
  try {
    const binary = atob(value)
    const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0))
    return new TextDecoder('utf-8').decode(bytes)
  } catch (error) {
    return ''
  }
}

function getStageImage() {
  return stage.value?.pic ? getPublicAssetUrl(stage.value.pic, 'contents') : fallbackImage
}
</script>

<template>
  <section class="interaction-screen detail-screen">
    <div v-if="loading" class="detail-state">正在展开卷宗...</div>
    <div v-else-if="loadError" class="detail-state">{{ loadError }}</div>
    <div v-else-if="!stage" class="detail-state">未找到阶段详情</div>

    <div v-else class="detail-scroll">
      <section class="detail-hero">
        <div class="detail-hero__image">
          <img :src="getStageImage()" alt="" />
        </div>

        <div class="detail-hero__body">
          <h2>{{ stage.name }}</h2>
          <p>{{ shortIntro }}</p>
          <strong>第 {{ stage.year || 1 }} 年</strong>
          <span>{{ qualificationName }}{{ majorName ? `・${majorName}` : '' }}</span>
        </div>
      </section>

      <section class="detail-panel">
        <h3>背景故事</h3>
        <p>{{ storyText }}</p>
      </section>

      <section class="detail-panel">
        <h3>资质效果</h3>
        <div class="effect-list">
          <p><strong>修行速度</strong><span>+{{ Math.max(5, 35 - Number(stage.year || 1) * 3) }}%</span></p>
          <p><strong>路径阶段</strong><span>{{ stage.detail ? '含图文资料' : '基础卷宗' }}</span></p>
          <p><strong>解锁条件</strong><span>{{ qualificationName }}</span></p>
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.detail-screen {
  height: 100%;
  padding: 18px 18px 20px;
  overflow: hidden;
  color: var(--ink);
}

.detail-scroll {
  display: grid;
  align-content: start;
  gap: 12px;
  height: 100%;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0 0 10px;
  overscroll-behavior: contain;
  scrollbar-width: none;
}

.detail-scroll::-webkit-scrollbar {
  display: none;
}

.detail-hero,
.detail-panel {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--panel);
  box-shadow:
    inset 0 0 18px rgba(255, 255, 255, 0.34),
    0 10px 24px var(--shadow-soft);
}

.detail-hero {
  display: grid;
  grid-template-columns: 44% minmax(0, 1fr);
  min-height: 210px;
  overflow: hidden;
}

.detail-hero__image {
  position: relative;
  min-height: 100%;
  overflow: hidden;
}

.detail-hero__image::after {
  position: absolute;
  inset: 0;
  border-right: 1px solid rgba(91, 131, 118, 0.48);
  border-radius: 0 48% 48% 0;
  box-shadow: 12px 0 28px rgba(95, 157, 140, 0.16);
  content: "";
}

.detail-hero__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.82);
}

.detail-hero__body {
  display: grid;
  align-content: center;
  gap: 12px;
  min-width: 0;
  padding: 20px 18px;
}

.detail-hero h2 {
  margin: 0;
  color: var(--ink);
  font-family: var(--app-font);
  font-size: 34px;
  line-height: 1;
  letter-spacing: 0;
}

.detail-hero p {
  margin: 0;
  color: var(--ink-soft);
  font-size: 15px;
  line-height: 1.75;
}

.detail-hero strong,
.detail-hero span {
  color: var(--green);
  font-size: 15px;
  font-weight: 900;
}

.detail-panel {
  padding: 18px 18px 20px;
}

.detail-panel h3 {
  margin: 0 0 14px;
  color: var(--ink);
  font-family: var(--app-font);
  font-size: 25px;
  line-height: 1;
  text-align: center;
}

.detail-panel p {
  margin: 0;
  color: var(--ink-soft);
  font-size: 15px;
  line-height: 1.85;
}

.effect-list {
  display: grid;
  gap: 12px;
}

.effect-list p {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  align-items: center;
  min-height: 38px;
  padding: 0 12px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.34);
}

.effect-list strong {
  color: var(--ink);
}

.effect-list span {
  color: var(--green);
  font-weight: 900;
}

.detail-state {
  display: grid;
  height: 100%;
  place-items: center;
  color: var(--ink);
  font-family: var(--app-font);
  font-size: 24px;
}

@media (max-height: 760px) {
  .detail-screen {
    padding: 12px 16px 16px;
  }

  .detail-hero {
    min-height: 172px;
  }

  .detail-hero__body {
    gap: 8px;
    padding: 16px 14px;
  }

  .detail-hero h2 {
    font-size: 28px;
  }

  .detail-hero p,
  .detail-panel p {
    font-size: 13px;
    line-height: 1.65;
  }

  .detail-panel {
    padding: 14px;
  }
}
</style>
