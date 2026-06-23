<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeIndex = ref(0)
const dragOffset = ref(0)
const isDragging = ref(false)
const suppressClick = ref(false)

const cardStep = 196
const swipeThreshold = 64
const dragState = {
  pointerId: null,
  startX: 0,
  moved: false
}

const directions = [
  {
    id: 'sword',
    label: '剑修',
    intro: '极致输出，快意恩仇的道友。',
    trait: '高爆发 · 高机动 · 攻守兼备',
    motto: '执剑破云，锋芒自成道。',
    tone: 'sky'
  },
  {
    id: 'alchemy',
    label: '丹修',
    intro: '稳步发展，厚积薄发的道友。',
    trait: '稳定成长 · 辅助增益',
    motto: '炉火不息，万物皆可化机缘。',
    tone: 'jade'
  },
  {
    id: 'talisman',
    label: '符修',
    intro: '善于布局，掌控全局的道友。',
    trait: '远程控制 · 持续伤害',
    motto: '一笔落符，天地听令。',
    tone: 'violet'
  },
  {
    id: 'body',
    label: '体修',
    intro: '正面推进，抗压成势的道友。',
    trait: '高生存 · 强突破',
    motto: '炼骨为山，寸步不退。',
    tone: 'ember'
  },
  {
    id: 'array',
    label: '阵修',
    intro: '谋定后动，后发制人的道友。',
    trait: '全局掌控 · 团队增幅',
    motto: '一阵既起，万象归位。',
    tone: 'gold'
  },
  {
    id: 'arraay',
    label: '阵修2',
    intro: '谋定后动，后发制人的道友。',
    trait: '全局掌控 · 团队增幅',
    motto: '一阵既起，万象归位。',
    tone: 'gold'
  }
]

function wrapIndex(index) {
  return (index + directions.length) % directions.length
}

function getLoopOffset(index) {
  const total = directions.length
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
        :class="[`tone-${direction.tone}`, { active: activeIndex === index }]"
        :style="getCardStyle(index)"
        @click="onCardClick(index)"
      >
        <div class="path-card__scene" aria-hidden="true">
          <i class="mountain mountain-left"></i>
          <i class="mountain mountain-right"></i>
          <b class="aura"></b>
          <b class="figure"></b>
        </div>

        <div class="path-card__content">
          <span class="path-card__seal">{{ String(index + 1).padStart(2, '0') }}</span>
          <h2>{{ direction.label }}</h2>
          <p class="path-card__trait">终点 {{ direction.trait }}</p>
          <p class="path-card__intro">{{ direction.intro }}</p>
          <strong>{{ direction.motto }}</strong>
          <button type="button" @click.stop="goIntake">查看详情</button>
        </div>
      </article>
    </section>

    <footer class="direction-footer">
      <div class="swipe-hint" aria-hidden="true">
        <span></span>
        <p>左右滑动选择</p>
      </div>

      <div class="path-steps" :style="{ '--step-count': directions.length }" aria-label="修行路径">
        <button
          v-for="(direction, index) in directions"
          :key="direction.id"
          type="button"
          class="path-step"
          :class="{ active: activeIndex === index }"
          :aria-label="`查看${direction.label}`"
          @click="selectDirection(index)"
        >
          <span>{{ index + 1 }}</span>
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
  top: 12px;
  bottom: 14px;
  left: 50%;
  display: grid;
  width: min(74vw, 318px);
  overflow: hidden;
  border: 1px solid rgba(250, 223, 159, 0.74);
  border-radius: 24px;
  color: #ffffff;
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

.path-card.tone-sky {
  background:
    linear-gradient(180deg, rgba(242, 250, 255, 0.78), rgba(85, 137, 183, 0.34) 48%, rgba(18, 42, 68, 0.86)),
    radial-gradient(circle at 50% 42%, rgba(174, 215, 255, 0.9), transparent 28%),
    #8ebfe6;
}

.path-card.tone-jade {
  background:
    linear-gradient(180deg, rgba(204, 237, 221, 0.7), rgba(60, 118, 96, 0.48) 52%, rgba(11, 37, 32, 0.9)),
    radial-gradient(circle at 48% 55%, rgba(115, 224, 164, 0.78), transparent 24%),
    #386b5d;
}

.path-card.tone-violet {
  background:
    linear-gradient(180deg, rgba(220, 214, 248, 0.72), rgba(100, 78, 150, 0.52) 50%, rgba(36, 25, 58, 0.92)),
    radial-gradient(circle at 54% 56%, rgba(178, 139, 242, 0.78), transparent 26%),
    #5a5188;
}

.path-card.tone-ember {
  background:
    linear-gradient(180deg, rgba(252, 219, 181, 0.72), rgba(151, 87, 45, 0.52) 50%, rgba(55, 26, 18, 0.92)),
    radial-gradient(circle at 50% 58%, rgba(255, 138, 73, 0.7), transparent 26%),
    #80492f;
}

.path-card.tone-gold {
  background:
    linear-gradient(180deg, rgba(250, 232, 184, 0.72), rgba(153, 119, 58, 0.5) 50%, rgba(50, 38, 21, 0.92)),
    radial-gradient(circle at 50% 55%, rgba(255, 219, 123, 0.72), transparent 28%),
    #8e6d3e;
}

.path-card::before {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  content: "";
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.3), transparent 22%, transparent 64%, rgba(10, 24, 42, 0.78)),
    radial-gradient(circle at 50% 34%, rgba(255, 255, 255, 0.54), transparent 24%);
}

.path-card__scene {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.mountain,
.aura,
.figure {
  position: absolute;
  display: block;
  pointer-events: none;
}
.path-card__content {
  position: relative;
  z-index: 2;
  display: grid;
  align-content: start;
  min-height: 100%;
  padding: 28px 24px 24px;
  text-align: center;
}

.path-card__seal {
  justify-self: start;
  color: rgba(255, 247, 222, 0.78);
  font-family: Georgia, serif;
  font-size: 13px;
  font-weight: 900;
}

.path-card__content h2 {
  margin: 12px 0 0;
  color: #173d72;
  font-family: "STKaiti", "KaiTi", "Songti SC", serif;
  font-size: 64px;
  line-height: 0.95;
  letter-spacing: 0;
  text-shadow: 0 2px 0 rgba(255, 255, 255, 0.34);
  writing-mode: vertical-rl;
  justify-self: center;
}

.path-card__trait {
  align-self: end;
  margin: auto 0 0;
  color: #f7f0de;
  font-size: 14px;
  font-weight: 900;
  line-height: 1.6;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.46);
}

.path-card__intro {
  margin: 8px 0 0;
  color: rgba(255, 255, 255, 0.88);
  font-size: 13px;
  line-height: 1.65;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
}

.path-card__content strong {
  margin-top: 8px;
  color: #ffffff;
  font-size: 15px;
  line-height: 1.5;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.42);
}

.path-card__content button {
  justify-self: center;
  min-width: 154px;
  min-height: 44px;
  margin-top: 18px;
  border: 1px solid #d2a96a;
  border-radius: 999px;
  color: #6c4423;
  background: linear-gradient(180deg, #fff7e8, #d9c19b);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.68),
    0 6px 14px rgba(37, 21, 10, 0.22);
  font-family: "STKaiti", "KaiTi", "Songti SC", serif;
  font-size: 18px;
  font-weight: 900;
}

.direction-footer {
  position: relative;
  z-index: 5;
  display: grid;
  justify-items: center;
  gap: 14px;
  padding: 0 16px;
  background: transparent;
  pointer-events: none;
}

.direction-footer button {
  pointer-events: auto;
}

.swipe-hint {
  display: grid;
  justify-items: center;
  gap: 5px;
  color: #f3ead9;
  font-family: "STKaiti", "KaiTi", "Songti SC", serif;
  font-size: 18px;
  text-shadow: 0 0 12px rgba(255, 232, 186, 0.22);
}

.swipe-hint span {
  width: 168px;
  height: 1px;
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
  gap: 4px;
  width: min(100%, 340px);
  margin: 0 auto;
}

.path-steps::before {
  position: absolute;
  top: 18px;
  right: 18px;
  left: 18px;
  height: 2px;
  background: linear-gradient(90deg, rgba(255, 215, 134, 0.9), rgba(230, 238, 238, 0.42));
  content: "";
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
  width: 38px;
  height: 38px;
  place-items: center;
  border: 1px solid rgba(225, 239, 237, 0.45);
  border-radius: 50%;
  background: rgba(15, 27, 39, 0.52);
  box-shadow:
    inset 0 0 12px rgba(255, 255, 255, 0.1),
    0 0 10px rgba(255, 255, 255, 0.08);
  font-family: Georgia, serif;
  font-size: 19px;
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
    top: 8px;
    bottom: 8px;
  }

  .path-card__content h2 {
    font-size: 50px;
  }

  .path-card__scene .figure {
    height: 142px;
  }

  .path-card__content button {
    min-height: 38px;
    margin-top: 10px;
  }

  .swipe-hint {
    display: none;
  }

  .path-step span {
    width: 34px;
    height: 34px;
    font-size: 17px;
  }

  .path-steps::before {
    top: 16px;
  }
}
</style>
