<script setup>
defineProps({
  tasks: {
    type: Array,
    default: () => [],
  },
  busy: {
    type: Boolean,
    default: false,
  },
  selectedId: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['refresh', 'select'])

function formatTime(value) {
  if (!value) return '未完成'

  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

function statusLabel(status) {
  const labels = {
    running: '处理中',
    success: '成功',
    failed: '失败',
  }
  return labels[status] || status
}
</script>

<template>
  <section class="history-panel">
    <div class="history-heading">
      <div>
        <p class="eyebrow">History</p>
        <h2>匿名历史记录</h2>
      </div>
      <button class="ghost-action" type="button" :disabled="busy" @click="emit('refresh')">
        {{ busy ? '刷新中' : '刷新' }}
      </button>
    </div>

    <div v-if="busy && tasks.length === 0" class="history-empty">
      正在加载历史记录
    </div>

    <div v-else-if="tasks.length === 0" class="history-empty">
      暂无历史记录，完成一次润色后会自动保存。
    </div>

    <div v-else class="history-list">
      <button
        v-for="task in tasks"
        :key="task.id"
        type="button"
        class="history-item"
        :class="[{ active: selectedId === task.id }, task.status]"
        @click="emit('select', task.id)"
      >
        <span class="history-title">
          <span class="history-id">#{{ task.id }}</span>
          <span>{{ task.requirement }}</span>
        </span>
        <span class="history-meta">
          <span class="history-status">{{ statusLabel(task.status) }}</span>
          <span>{{ task.model_name }}</span>
          <span>{{ formatTime(task.created_at) }}</span>
        </span>
      </button>
    </div>
  </section>
</template>
