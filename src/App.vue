<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router'
import AppShell from './components/AppShell.vue'

const route = useRoute()
const router = useRouter()

function handleShellClick() {
  if (route.name === 'home') {
    router.push('/directions')
  }
}
</script>

<template>
  <AppShell>
    <section class="route-touch-area" @click="handleShellClick">
      <RouterView v-slot="{ Component }">
        <component :is="Component" />
      </RouterView>
    </section>
  </AppShell>
</template>

<style scoped>
.route-touch-area {
  height: 100%;
  min-height: 0;
}
</style>
