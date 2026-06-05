<script setup>
defineProps({
  status: {
    type: Object,
    required: true,
  },
  busy: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <header class="status-bar">
    <div>
      <p class="eyebrow">AI Paper Polishing Agent</p>
      <h1>论文润色 Agent</h1>
    </div>
    <div class="status-group">
      <span class="mode">Vue + FastAPI</span>
      <span class="status-pill" :class="{ online: status.ok, offline: !status.ok }">
        <span class="status-dot"></span>
        {{ busy ? '处理中' : status.label }}
      </span>
    </div>
  </header>
</template>
