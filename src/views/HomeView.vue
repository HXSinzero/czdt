<template>
  <section
    class="tap-home interaction-screen"
    aria-hidden="true"
    aria-label="进入方向选择页"
  >
    <div class="interaction-placeholder">
      <span>Home</span>
      <strong>首页触达区</strong>
      <p>点击任意位置进入方向选择页。</p>
    </div>
  </section>
</template>

<style scoped>
.tap-home {
  display: grid;
  place-items: center;
  padding: 24px;
  border: 0;
  border-radius: 0;
  outline: none;
  background: transparent;
  touch-action: manipulation;
}

.tap-home:focus-visible {
  box-shadow: inset 0 0 0 3px rgba(35, 103, 209, 0.42);
}

.interaction-placeholder {
  display: grid;
  justify-items: center;
  gap: 10px;
  width: min(100%, 300px);
  color: var(--ink);
  text-align: center;
}

.interaction-placeholder span {
  color: var(--green);
  font-size: 13px;
  font-weight: 900;
  text-transform: uppercase;
}

.interaction-placeholder strong {
  font-size: 28px;
  letter-spacing: 0;
}

.interaction-placeholder p {
  margin: 0;
  color: var(--ink-soft);
  line-height: 1.7;
}
</style>
