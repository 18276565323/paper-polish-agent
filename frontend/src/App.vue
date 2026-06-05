<script setup>
import { onMounted, ref } from 'vue'

import { checkHealth, polishPaper } from './api/polish'
import DetailTabs from './components/DetailTabs.vue'
import InputPanel from './components/InputPanel.vue'
import ResultPanel from './components/ResultPanel.vue'
import StatusBar from './components/StatusBar.vue'

const text = ref('本文提出了一种方法，该方法可以提高系统性能。')
const requirement = ref('学术化润色')
const result = ref(null)
const errorMessage = ref('')
const busy = ref(false)
const backendStatus = ref({ ok: false, label: '检测中' })

async function refreshHealth() {
  backendStatus.value = await checkHealth()
}

async function submitPolish() {
  if (!text.value.trim() || busy.value) return

  busy.value = true
  errorMessage.value = ''

  try {
    result.value = await polishPaper({
      text: text.value.trim(),
      requirement: requirement.value,
    })
    await refreshHealth()
  } catch (error) {
    errorMessage.value = error.message || '请求失败'
  } finally {
    busy.value = false
  }
}

onMounted(refreshHealth)
</script>

<template>
  <main class="app-shell">
    <StatusBar :status="backendStatus" :busy="busy" />

    <section v-if="errorMessage" class="error-banner">
      {{ errorMessage }}
    </section>

    <section class="workspace">
      <InputPanel
        v-model:text="text"
        v-model:requirement="requirement"
        :busy="busy"
        @submit="submitPolish"
      />
      <ResultPanel :result="result" :busy="busy" />
    </section>

    <DetailTabs :result="result" />
  </main>
</template>
