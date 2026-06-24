<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPublicAssetUrl } from '../config'

const route = useRoute()
const router = useRouter()
const growthTree = ref([])
const loading = ref(true)
const loadError = ref('')
const fallbackImage = getPublicAssetUrl('contents/directions.webp')

const directionName = computed(() => String(route.query.direction || '').trim())
const qualificationName = computed(() => String(route.query.qualification || '').trim())
const majorName = computed(() => String(route.query.major || '').trim())

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
const stages = computed(() => {
  const children = selectedQualification.value?.children || []
  return [...children].sort((a, b) => Number(a.year || 0) - Number(b.year || 0))
})
const timelineGroups = computed(() => {
  const groups = []

  stages.value.forEach((stage) => {
    const year = Number(stage.year || 1)
    const lastGroup = groups[groups.length - 1]

    if (lastGroup?.year === year) {
      lastGroup.stages.push(stage)
      return
    }

    groups.push({
      year,
      stages: [stage]
    })
  })

  return groups
})
const totalYears = computed(() => stages.value.reduce((max, stage) => Math.max(max, Number(stage.year || 0)), 0))
const currentRealm = computed(() => {
  const last = stages.value[stages.value.length - 1]
  return last?.name ? `${last.name}・中期` : '未定'
})

onMounted(async () => {
  try {
    const response = await fetch(getPublicAssetUrl('contents/data.json'))
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    growthTree.value = await response.json()
  } catch (error) {
    loadError.value = '路线暂未载入'
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

function getStageIntro(stage) {
  const text = decodeBase64Text(stage.txt).replace(/\s+/g, ' ').trim()
  if (!text) return '此境界卷宗待补，先以稳扎稳打为要。'
  return text.slice(0, 42)
}

function getStageImage(stage) {
  return stage.pic ? getPublicAssetUrl(stage.pic, 'contents') : fallbackImage
}

function goStageDetail(stage) {
  router.push({
    path: '/stage-detail',
    query: {
      direction: directionName.value,
      qualification: qualificationName.value,
      major: majorName.value,
      stage: stage.name,
      year: stage.year || 1
    }
  })
}
</script>

<template>
  <section class="interaction-screen timeline-screen">
    <div v-if="loading" class="timeline-state">正在推演年限...</div>
    <div v-else-if="loadError" class="timeline-state">{{ loadError }}</div>
    <div v-else-if="!selectedQualification" class="timeline-state">未找到对应路线</div>

    <div v-else class="timeline-content">
      <section class="realm-summary">
        <p>当前修行：第 <strong>{{ totalYears || 1 }}</strong> 年</p>
        <p>境界：<strong>{{ currentRealm }}</strong></p>
      </section>

      <section class="timeline-scroll" aria-label="路线总览">
        <div
          v-for="group in timelineGroups"
          :key="group.year"
          class="timeline-group"
        >
          <div class="year-mark">第 {{ group.year }} 年</div>

          <div class="stage-group">
            <button
              v-for="stage in group.stages"
              :key="`${stage.name}-${stage.year}`"
              type="button"
              class="stage-card"
              :class="{ featured: stages[0] === stage }"
              @click="goStageDetail(stage)"
            >
              <img class="stage-card__image" :src="getStageImage(stage)" alt="" />
              <div class="stage-card__body">
                <h2>{{ stage.name }}</h2>
                <p>{{ getStageIntro(stage) }}</p>
              </div>
            </button>
          </div>
        </div>
      </section>

      <footer class="timeline-total">
        <span></span>
        <p>总计：<strong>{{ stages.length }}</strong> 个阶段</p>
        <span></span>
      </footer>
    </div>
  </section>
</template>

<style scoped>
.timeline-screen {
  position: relative;
  height: 100%;
  margin: 0;
  padding: 34px 14px 18px;
  overflow: hidden;
  color: #fff4dc;
}

.timeline-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  gap: 14px;
  height: 100%;
  min-height: 0;
}

.realm-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  min-height: 54px;
  align-items: center;
  padding: 0 14px;
  border-radius: 8px;
  color: #fff5df;
  background: rgba(37, 57, 72, 0.72);
  box-shadow: inset 0 0 18px rgba(255, 255, 255, 0.04);
}

.realm-summary p {
  min-width: 0;
  overflow: hidden;
  margin: 0;
  font-family: var(--app-font);
  font-size: 16px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.realm-summary p:last-child {
  text-align: right;
}

.realm-summary strong {
  color: #56b566;
  font-weight: 900;
}

.timeline-scroll {
  position: relative;
  display: grid;
  align-content: start;
  gap: 16px;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 4px 0 8px;
  overscroll-behavior: contain;
  scrollbar-width: none;
}

.timeline-scroll::-webkit-scrollbar {
  display: none;
}

.timeline-scroll::before {
  position: absolute;
  top: 72px;
  bottom: 72px;
  left: 65px;
  width: 1px;
  background: linear-gradient(180deg, transparent, #c99142 16%, #c99142 84%, transparent);
  box-shadow: 0 0 14px rgba(255, 197, 100, 0.58);
  content: "";
}

.timeline-group {
  position: relative;
  display: grid;
  grid-template-columns: 78px minmax(0, 1fr);
  align-items: center;
  min-height: 142px;
}

.timeline-group + .timeline-group::before {
  position: absolute;
  top: -8px;
  right: 0;
  left: 92px;
  height: 2px;
  overflow: hidden;
  background: linear-gradient(90deg, transparent, rgba(255, 218, 148, 0.78), rgba(255, 218, 148, 0.22), transparent);
  box-shadow:
    0 0 10px rgba(255, 202, 106, 0.48),
    0 0 18px rgba(255, 232, 172, 0.2);
  content: "";
}

.year-mark {
  position: relative;
  z-index: 2;
  padding-right: 18px;
  color: #ffd890;
  font-family: var(--app-font);
  font-size: 17px;
  text-align: right;
  white-space: nowrap;
}

.year-mark::after {
  position: absolute;
  top: 50%;
  right: 7px;
  width: 10px;
  height: 10px;
  border: 1px solid #fff0c4;
  background: rgba(172, 111, 39, 0.86);
  box-shadow: 0 0 12px rgba(255, 207, 113, 0.8);
  content: "";
  transform: translateY(-50%) rotate(45deg);
}

.stage-group {
  display: grid;
  gap: 12px;
  min-width: 0;
}

.stage-card {
  position: relative;
  display: grid;
  grid-template-columns: 38% minmax(0, 1fr);
  width: 100%;
  min-width: 0;
  height: 142px;
  min-height: 0;
  padding: 0;
  overflow: hidden;
  border: 1px solid rgba(241, 218, 169, 0.22);
  border-radius: 8px;
  color: inherit;
  background: rgba(33, 52, 66, 0.66);
  box-shadow:
    inset 0 0 18px rgba(255, 255, 255, 0.04),
    0 10px 24px rgba(1, 9, 16, 0.22);
  text-align: left;
}

.stage-card.featured {
  border-color: rgba(255, 226, 158, 0.92);
  box-shadow:
    0 0 0 1px rgba(255, 238, 190, 0.48),
    0 0 20px rgba(255, 203, 105, 0.68),
    inset 0 0 18px rgba(255, 241, 202, 0.08);
}

.stage-card__image {
  width: 100%;
  height: 100%;
  min-height: 0;
  object-fit: cover;
  filter: saturate(0.8);
}

.stage-card__body {
  display: grid;
  align-content: center;
  gap: 14px;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
  padding: 18px 14px;
  border-left: 1px solid rgba(255, 239, 198, 0.12);
}

.stage-card h2 {
  min-width: 0;
  overflow: hidden;
  margin: 0;
  color: #fff0d2;
  font-family: var(--app-font);
  font-size: 26px;
  line-height: 1;
  letter-spacing: 0;
  white-space: nowrap;
}

.stage-card p {
  margin: 0;
  color: rgba(255, 245, 224, 0.84);
  font-size: 14px;
  line-height: 1.65;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}

.timeline-total {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 18px;
  color: #fff4dc;
  font-family: var(--app-font);
  font-size: 22px;
}

.timeline-total span {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(247, 222, 166, 0.66));
}

.timeline-total span:last-child {
  background: linear-gradient(90deg, rgba(247, 222, 166, 0.66), transparent);
}

.timeline-total p {
  margin: 0;
  white-space: nowrap;
}

.timeline-total strong {
  color: #56b566;
}

.timeline-state {
  display: grid;
  height: 100%;
  place-items: center;
  color: #fff2d7;
  font-family: var(--app-font);
  font-size: 24px;
}

@media (max-height: 760px) {
  .timeline-screen {
    padding-top: 22px;
  }

  .timeline-content {
    gap: 10px;
  }

  .realm-summary {
    min-height: 48px;
  }

  .realm-summary p {
    font-size: 15px;
  }

  .timeline-scroll {
    gap: 12px;
  }

  .timeline-scroll::before {
    left: 53px;
  }

  .timeline-group {
    grid-template-columns: 64px minmax(0, 1fr);
    min-height: 116px;
  }

  .timeline-group + .timeline-group::before {
    left: 76px;
    top: -6px;
  }

  .year-mark {
    padding-right: 14px;
    font-size: 14px;
  }

  .year-mark::after {
    right: 4px;
    width: 8px;
    height: 8px;
  }

  .stage-card {
    height: 116px;
  }

  .stage-card__body {
    gap: 10px;
    padding: 14px 12px;
  }

  .stage-card h2 {
    font-size: 25px;
  }

  .stage-card p {
    font-size: 13px;
    line-height: 1.55;
  }

  .timeline-total {
    font-size: 18px;
  }
}
</style>
