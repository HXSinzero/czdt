<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getPublicAssetUrl } from '../config'

const router = useRouter()
const activeIndex = ref(0)
const dragOffset = ref(0)
const isDragging = ref(false)
const suppressClick = ref(false)
const cards = ref([])

const cardStep = 196
const swipeThreshold = 64
const cardsBaseDir = 'contents'
const dragState = {
  pointerId: null,
  startX: 0,
  moved: false
}

const tones = ['sky', 'jade', 'violet', 'ember', 'gold']
const imagePattern = /\.(png|jpe?g|webp|gif|bmp|svg)(\?.*)?$/i
const directions = computed(() => cards.value.map((card, index) => ({
  id: card.id || card.title || `card-${index}`,
  label: card.title,
  intro: card.discription || '',
  trait: card.subtitle || '',
  motto: card.motto || card.subtitle || '',
  pic: card.pic || '',
  stamp: card.stamp || '',
  tone: card.tone || tones[index % tones.length]
})))

onMounted(async () => {
  const response = await fetch(getPublicAssetUrl('contents/cards.json'))
  cards.value = await response.json()
})

function isImagePath(value) {
  return typeof value === 'string' && imagePattern.test(value)
}

function wrapIndex(index) {
  const total = directions.value.length
  if (!total) return 0
  return (index + total) % total
}

function getLoopOffset(index) {
  const total = directions.value.length
  let offset = index - activeIndex.value

  if (offset > total / 2) offset -= total
  if (offset < -total / 2) offset += total

  return offset
}

function getCardStyle(index) {
  const baseOffset = getLoopOffset(index)
  const dragProgress = dragOffset.value / cardStep
  const offset = baseOffset + dragProgress
  const distance = Math.min(Math.abs(offset), 2.2)
  const side = Math.sign(offset)
  const hidden = Math.abs(offset) > 2.25

  return {
    zIndex: String(100 - Math.round(distance * 10)),
    opacity: hidden ? 0 : 1 - Math.max(0, distance - 1.7) * 1.4,
    pointerEvents: hidden ? 'none' : 'auto',
    transform: [
      'translateX(-50%)',
      `translateX(${offset * cardStep}px)`,
      `translateZ(${-distance * 70}px)`,
      `rotateY(${side * -16 * Math.min(distance, 1)}deg)`,
      `scale(${1 - distance * 0.11})`
    ].join(' ')
  }
}

function selectDirection(index) {
  activeIndex.value = wrapIndex(index)
  dragOffset.value = 0
}

function goPrev() {
  selectDirection(activeIndex.value - 1)
}

function goNextPath() {
  selectDirection(activeIndex.value + 1)
}

function onPointerDown(event) {
  dragState.pointerId = event.pointerId
  dragState.startX = event.clientX
  dragState.moved = false
  isDragging.value = true
  event.currentTarget.setPointerCapture(event.pointerId)
}

function onPointerMove(event) {
  if (dragState.pointerId !== event.pointerId) return

  const delta = event.clientX - dragState.startX
  if (Math.abs(delta) > 4) {
    dragState.moved = true
    suppressClick.value = true
  }

  if (!dragState.moved) return

  dragOffset.value = Math.max(Math.min(delta, cardStep), -cardStep)
}

function onPointerUp(event) {
  if (dragState.pointerId !== event.pointerId) return

  event.currentTarget.releasePointerCapture(event.pointerId)
  isDragging.value = false

  if (dragOffset.value <= -swipeThreshold) {
    goNextPath()
  } else if (dragOffset.value >= swipeThreshold) {
    goPrev()
  } else {
    dragOffset.value = 0
  }

  window.setTimeout(() => {
    suppressClick.value = false
  }, 0)

  dragState.pointerId = null
}

function onCardClick(index) {
  if (suppressClick.value) return
  if (index !== activeIndex.value) {
    selectDirection(index)
  }
}

function goIntake() {
  router.push('/intake')
}

function getStepLabel(index) {
  return directions.value[index]?.label?.trim().charAt(0) || String(index + 1)
}

function getCardBackground(direction) {
  if (!isImagePath(direction.pic)) return {}

  return {
    backgroundImage: `url("${getPublicAssetUrl(direction.pic, cardsBaseDir)}")`
  }
}

function getCardImageUrl(path) {
  return getPublicAssetUrl(path, cardsBaseDir)
}
</script>

<template>
  <section class="interaction-screen direction-screen">
    <section
      class="carousel-stage"
      :class="{ dragging: isDragging }"
      aria-label="修行方向"
      @pointerdown="onPointerDown"
      @pointermove="onPointerMove"
      @pointerup="onPointerUp"
      @pointercancel="onPointerUp"
    >
      <article
        v-for="(direction, index) in directions"
        :key="direction.id"
        class="path-card"
        :class="{ active: activeIndex === index }"
        :style="[getCardStyle(index), getCardBackground(direction)]"
        @click="onCardClick(index)"
      >
        <div class="path-card__content">
          <img v-if="isImagePath(direction.stamp)" class="path-card__stamp" :src="getCardImageUrl(direction.stamp)" alt="" />
          <div class="path-card__title-zone">
            <h2>{{ direction.label }}</h2>
          </div>
          <div class="path-card__text-zone">
            <p class="path-card__trait">终点 {{ direction.trait }}</p>
            <p class="path-card__intro">{{ direction.intro }}</p>
            <strong>{{ direction.motto }}</strong>
          </div>
          <button type="button" @click.stop="goIntake">查看详情</button>
        </div>
      </article>
    </section>

    <footer class="direction-footer">
      <div class="swipe-hint" aria-hidden="true">
        <span></span>
        <p>左右滑动选择</p>
      </div>

      <div class="path-steps" :style="{ '--step-count': directions.length || 1 }" aria-label="修行路径">
        <button
          v-for="(direction, index) in directions"
          :key="direction.id"
          type="button"
          class="path-step"
          :class="{ active: activeIndex === index }"
          :aria-label="`查看${direction.label}`"
          @click="selectDirection(index)"
        >
          <span style="font-family: 'zydt';">{{ getStepLabel(index) }}</span>
        </button>
      </div>
    </footer>
  </section>
</template>

<style scoped>
.direction-screen {
  position: relative;
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  height: 100%;
  margin: 0;
  padding: 0 0 22px;
  overflow: hidden;
  color: #f8ecd5;
}

.carousel-stage {
  position: relative;
  z-index: 2;
  min-height: 0;
  overflow: hidden;
  perspective: 980px;
  touch-action: pan-y;
  cursor: grab;
  background: transparent;
}

.carousel-stage.dragging {
  cursor: grabbing;
}

.carousel-stage::before,
.carousel-stage::after {
  display: none;
}

.path-card {
  position: absolute;
  top: 30px;
  bottom: 34px;
  left: 50%;
  display: grid;
  width: min(74vw, 318px);
  overflow: hidden;
  border: 1px solid rgba(250, 223, 159, 0.74);
  border-radius: 24px;
  color: #ffffff;
  background-color: transparent;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  transform-style: preserve-3d;
  user-select: none;
  -webkit-user-select: none;
  box-shadow:
    inset 0 0 10px rgba(255, 255, 255, 0.12),
    0 3px 7px rgba(0, 0, 0, 0.26);
  transition:
    transform 220ms ease,
    opacity 220ms ease,
    box-shadow 220ms ease;
}

.path-card * {
  user-select: none;
  -webkit-user-select: none;
}

.carousel-stage.dragging .path-card {
  transition: none;
}

.path-card.active {
  box-shadow:
    0 0 0 1px rgba(255, 247, 211, 0.8),
    0 0 10px rgba(255, 225, 154, 0.88),
    0 7px 14px rgba(4, 10, 18, 0.48);
}

.path-card__content {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-rows: 230px minmax(0, 1fr) 112px;
  min-height: 100%;
  padding: 18px 24px 24px;
  text-align: center;
}

.path-card__stamp {
  position: absolute;
  top: 46px;
  right: 34px;
  width: 42px;
  height: 42px;
  object-fit: contain;
}

.path-card__title-zone {
  display: grid;
  min-height: 0;
  place-items: center;
}

.path-card__content h2 {
  margin: 0;
  color: #173d72;
  font-family: var(--app-font);
  font-size: 60px;
  line-height: 0.95;
  letter-spacing: 0;
  text-shadow: 0 2px 0 rgba(255, 255, 255, 0.34);
  writing-mode: vertical-rl;
  justify-self: center;
}

.path-card__text-zone {
  display: grid;
  min-height: 0;
  overflow: hidden;
  align-content: start;
}

.path-card__trait {
  align-self: end;
  margin: 0;
  color: #f7f0de;
  font-size: 17px;
  font-weight: 900;
  line-height: 1.6;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.46);
}

.path-card__intro {
  margin: 8px 0 0;
  color: rgba(255, 255, 255, 0.88);
  font-size: 15px;
  line-height: 1.7;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
}

.path-card__content strong {
  margin-top: 8px;
  color: #ffffff;
  font-size: 18px;
  line-height: 1.5;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.42);
}

.path-card__content button {
  align-self: center;
  justify-self: center;
  min-width: 174px;
  min-height: 50px;
  border: 1px solid #d2a96a;
  border-radius: 999px;
  color: #6c4423;
  background: linear-gradient(180deg, #fff7e8, #d9c19b);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.68),
    0 6px 14px rgba(37, 21, 10, 0.22);
  font-family: var(--app-font);
  font-size: 21px;
  font-weight: 900;
}

.direction-footer {
  position: relative;
  z-index: 5;
  display: grid;
  justify-items: center;
  gap: 18px;
  padding: 0 18px;
  background: transparent;
  pointer-events: none;
}

.direction-footer button {
  pointer-events: auto;
}

.swipe-hint {
  display: grid;
  justify-items: center;
  gap: 7px;
  color: #f3ead9;
  font-family: var(--app-font);
  font-size: 22px;
  text-shadow: 0 0 12px rgba(255, 232, 186, 0.22);
}

.swipe-hint span {
  width: 220px;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(246, 225, 177, 0.46), transparent);
}

.swipe-hint p {
  margin: 0;
  font-weight: 900;
}

.swipe-hint i {
  position: relative;
  width: 46px;
  height: 26px;
}

.swipe-hint i::before {
  position: absolute;
  inset: 5px 13px 0;
  border: 2px solid rgba(255, 255, 255, 0.54);
  border-top: 0;
  border-radius: 0 0 14px 14px;
  content: "";
}

.swipe-hint i::after {
  position: absolute;
  inset: 0;
  color: rgba(255, 255, 255, 0.58);
  content: "<  >";
  font-family: Georgia, serif;
  font-style: normal;
  font-weight: 800;
  letter-spacing: 10px;
  animation: hintSlide 1.35s ease-in-out infinite;
}

.path-steps {
  position: relative;
  display: grid;
  grid-template-columns: repeat(var(--step-count), 1fr);
  gap: 6px;
  width: min(100%, 390px);
  margin: 0 auto;
}

.path-step {
  position: relative;
  z-index: 1;
  display: grid;
  justify-items: center;
  min-width: 0;
  padding: 0;
  border: 0;
  color: rgba(248, 236, 213, 0.78);
  background: transparent;
}

.path-step span {
  display: grid;
  width: 50px;
  height: 50px;
  place-items: center;
  border: 1px solid rgba(225, 239, 237, 0.45);
  border-radius: 50%;
  background: rgba(15, 27, 39, 0.52);
  box-shadow:
    inset 0 0 12px rgba(255, 255, 255, 0.1),
    0 0 10px rgba(255, 255, 255, 0.08);
  font-family: Georgia, serif;
  font-size: 24px;
  font-weight: 900;
}

.path-step.active {
  color: #ffe7af;
}

.path-step.active span {
  border-color: #ffe2a2;
  background: rgba(64, 43, 20, 0.7);
  box-shadow:
    0 0 0 2px rgba(255, 235, 177, 0.22),
    0 0 18px rgba(255, 207, 105, 0.86),
    inset 0 0 16px rgba(255, 242, 193, 0.28);
}

@keyframes hintSlide {
  0%,
  100% {
    transform: translateX(0);
  }

  50% {
    transform: translateX(6px);
  }
}

@media (max-height: 760px) {
  .direction-screen {
    padding-bottom: 14px;
  }

  .path-card {
    width: min(70vw, 300px);
    top: 18px;
    bottom: 20px;
  }

  .path-card__content {
    grid-template-rows: 188px minmax(0, 1fr) 86px;
    padding: 14px 22px 18px;
  }

  .path-card__content h2 {
    font-size: 60px;
  }

  .path-card__content button {
    min-height: 42px;
    min-width: 150px;
    font-size: 18px;
  }

  .swipe-hint {
    display: none;
  }

  .path-step span {
    width: 42px;
    height: 42px;
    font-size: 20px;
  }
}
</style>
