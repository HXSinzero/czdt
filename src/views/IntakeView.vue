<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPublicAssetUrl } from '../config'

const route = useRoute()
const router = useRouter()
const growthTree = ref([])
const loading = ref(true)
const loadError = ref('')
const isRelatedMajor = ref(true)
const sceneImage = `url("${getPublicAssetUrl('contents/directions.webp')}")`

const selectedDirectionName = computed(() => String(route.query.direction || '').trim())
const selectedDirection = computed(() => {
  if (!selectedDirectionName.value) return null
  return growthTree.value.find((item) => item.name === selectedDirectionName.value) || null
})
const rawQualifications = computed(() => selectedDirection.value?.children || [])
const hasMajorFilter = computed(() => rawQualifications.value.some((item) => item.root === false))
const qualifications = computed(() => rawQualifications.value.map(resolveQualification))

onMounted(async () => {
  try {
    const response = await fetch(getPublicAssetUrl('contents/data.json'))
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    growthTree.value = await response.json()
  } catch (error) {
    loadError.value = '资料暂未载入'
  } finally {
    loading.value = false
  }
})

function getQualificationIntro(qualification) {
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
  <section class="interaction-screen qualification-screen">
    <div v-if="loading" class="qualification-state">正在翻阅卷宗...</div>
    <div v-else-if="loadError" class="qualification-state">{{ loadError }}</div>
    <div v-else-if="!selectedDirection" class="qualification-state">未找到对应方向</div>

    <div v-else class="qualification-content">
      <label v-if="hasMajorFilter" class="major-filter">
        <input v-model="isRelatedMajor" type="checkbox" />
        <span>相关专业</span>
      </label>

      <div class="qualification-list" aria-label="学历选择">
      <article
        v-for="(qualification, index) in qualifications"
        :key="qualification.name"
        class="qualification-card"
        :class="{ featured: index === 0 }"
        :style="{ '--scene-image': sceneImage }"
      >
        <div class="qualification-card__scene" aria-hidden="true"></div>

        <div class="qualification-card__body">
          <h2>{{ qualification.name }}</h2>
          <small v-if="qualification.major">{{ qualification.major }}</small>
          <p>{{ getQualificationIntro(qualification) }}</p>
          <strong>
            <span>✽</span>
            {{ getSpeedLabel(qualification, index) }}
          </strong>
        </div>

        <button type="button" @click="selectQualification(qualification)">选择此资质</button>
      </article>
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
  color: #fff5df;
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
  border: 1px solid rgba(246, 216, 153, 0.5);
  border-radius: 999px;
  color: #f9e9c9;
  background: rgba(12, 21, 31, 0.32);
  box-shadow:
    inset 0 0 12px rgba(255, 244, 204, 0.1),
    0 0 14px rgba(244, 196, 101, 0.18);
  font-family: var(--app-font);
  font-size: 18px;
  font-weight: 900;
}

.major-filter input {
  width: 18px;
  height: 18px;
  margin: 0;
  accent-color: #d8b36f;
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
  grid-template-columns: 42% minmax(0, 1fr);
  min-height: 132px;
  overflow: hidden;
  border: 1px solid rgba(241, 218, 169, 0.34);
  border-radius: 8px;
  background:
    linear-gradient(90deg, rgba(11, 23, 35, 0.1), rgba(19, 34, 48, 0.92) 42%, rgba(30, 48, 64, 0.88)),
    rgba(16, 29, 42, 0.9);
  box-shadow:
    inset 0 0 20px rgba(255, 255, 255, 0.05),
    0 10px 24px rgba(2, 9, 17, 0.24);
}

.qualification-card.featured {
  border-color: rgba(255, 230, 176, 0.98);
  box-shadow:
    0 0 0 1px rgba(255, 245, 204, 0.58),
    0 0 20px rgba(255, 209, 120, 0.72),
    inset 0 0 18px rgba(255, 239, 195, 0.1);
}

.qualification-card__scene {
  min-height: 100%;
  background:
    linear-gradient(90deg, rgba(13, 26, 39, 0.05), rgba(17, 30, 42, 0.74)),
    var(--scene-image) center / cover;
  filter: saturate(0.82);
}

.qualification-card:nth-child(2n) .qualification-card__scene {
  filter: saturate(0.7) hue-rotate(18deg);
}

.qualification-card:nth-child(3n) .qualification-card__scene {
  filter: saturate(0.78) hue-rotate(48deg);
}

.qualification-card__body {
  display: grid;
  align-content: center;
  min-width: 0;
  padding: 16px 18px 54px;
}

.qualification-card h2 {
  margin: 0;
  color: #fff0d5;
  font-family: var(--app-font);
  font-size: 32px;
  line-height: 1;
  letter-spacing: 0;
  text-shadow: 0 0 12px rgba(255, 230, 178, 0.18);
}

.qualification-card small {
  margin-top: 4px;
  color: #8ed18f;
  font-size: 13px;
  font-weight: 900;
  line-height: 1;
}

.qualification-card p {
  margin: 10px 0 0;
  color: rgba(255, 245, 225, 0.82);
  font-size: 14px;
  line-height: 1.55;
}

.qualification-card strong {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  color: #8ed18f;
  font-size: 14px;
  line-height: 1;
}

.qualification-card strong span {
  display: grid;
  width: 20px;
  height: 20px;
  place-items: center;
  border-radius: 50%;
  color: #ffffff;
  background: rgba(103, 147, 189, 0.9);
  font-size: 12px;
}

.qualification-card button {
  position: absolute;
  right: 16px;
  bottom: 18px;
  min-width: 112px;
  min-height: 34px;
  padding: 0 16px;
  border: 1px solid rgba(138, 104, 62, 0.68);
  border-radius: 4px;
  color: #6d4420;
  background:
    linear-gradient(135deg, transparent 8px, #d7c49f 0) top left,
    linear-gradient(225deg, transparent 8px, #d7c49f 0) top right,
    linear-gradient(315deg, transparent 8px, #d7c49f 0) bottom right,
    linear-gradient(45deg, transparent 8px, #d7c49f 0) bottom left;
  background-size: 51% 51%;
  background-repeat: no-repeat;
  font-family: var(--app-font);
  font-size: 16px;
  font-weight: 900;
  box-shadow: inset 0 0 0 1px rgba(255, 246, 217, 0.4);
}

.qualification-state {
  display: grid;
  height: 100%;
  place-items: center;
  color: #fff2d7;
  font-family: var(--app-font);
  font-size: 24px;
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
    padding: 12px 14px 46px;
  }

  .qualification-card h2 {
    font-size: 27px;
  }

  .qualification-card p,
  .qualification-card strong {
    font-size: 12px;
  }

  .qualification-card button {
    right: 12px;
    bottom: 12px;
    min-width: 96px;
    min-height: 30px;
    font-size: 14px;
  }
}
</style>
