<script setup>
import { onMounted, ref } from 'vue'

import { checkHealth, getTaskDetail, listTasks, polishPaper } from './api/polish'
import DetailTabs from './components/DetailTabs.vue'
import HistoryPanel from './components/HistoryPanel.vue'
import InputPanel from './components/InputPanel.vue'
import ResultPanel from './components/ResultPanel.vue'
import StatusBar from './components/StatusBar.vue'

const text = ref('本文提出了一种方法，该方法可以提高系统性能。')
const requirement = ref('学术化润色')
const result = ref(null)
const errorMessage = ref('')
const busy = ref(false)
const historyBusy = ref(false)
const selectedTaskId = ref(null)
const tasks = ref([])
const backendStatus = ref({ ok: false, label: '检测中' })

async function refreshHealth() {
  backendStatus.value = await checkHealth()
}

async function refreshTasks() {
  historyBusy.value = true

  try {
    tasks.value = await listTasks(20)
  } catch (error) {
    errorMessage.value = error.message || '历史记录加载失败'
  } finally {
    historyBusy.value = false
  }
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
    selectedTaskId.value = null
    await Promise.all([refreshHealth(), refreshTasks()])
  } catch (error) {
    errorMessage.value = error.message || '请求失败'
    await refreshTasks()
  } finally {
    busy.value = false
  }
}

async function selectTask(taskId) {
  if (historyBusy.value) return

  historyBusy.value = true
  errorMessage.value = ''

  try {
    const task = await getTaskDetail(taskId)
    selectedTaskId.value = task.id
    text.value = task.input_text
    requirement.value = task.requirement
    result.value = task.result_json
    if (task.status === 'failed') {
      errorMessage.value = task.error_message || '这条历史任务执行失败'
    }
  } catch (error) {
    errorMessage.value = error.message || '历史详情加载失败'
  } finally {
    historyBusy.value = false
  }
}

onMounted(() => {
  refreshHealth()
  refreshTasks()
})
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

    <section class="lower-grid">
      <DetailTabs :result="result" />
      <HistoryPanel
        :tasks="tasks"
        :busy="historyBusy"
        :selected-id="selectedTaskId"
        @refresh="refreshTasks"
        @select="selectTask"
      />
    </section>
  </main>
</template>
