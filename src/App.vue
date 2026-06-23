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
  <AppShell @click="handleShellClick">
    <RouterView v-slot="{ Component }">
      <component :is="Component" />
    </RouterView>
  </AppShell>
</template>
