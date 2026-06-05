<script setup>
defineProps({
  result: {
    type: Object,
    default: null,
  },
  busy: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <section class="panel result-panel">
    <div class="panel-heading">
      <div>
        <p class="eyebrow">Result</p>
        <h2>润色结果</h2>
      </div>
    </div>

    <div v-if="busy" class="state-block">
      <div class="loading-line"></div>
      <div class="loading-line short"></div>
      <div class="loading-line"></div>
    </div>

    <div v-else-if="result" class="result-content">
      <article>
        <h3>优化后文本</h3>
        <p>{{ result.polish_text }}</p>
      </article>
      <article>
        <h3>原文</h3>
        <p>{{ result.original_text }}</p>
      </article>
    </div>

    <div v-else class="state-block empty">
      <p>等待输入论文文本</p>
    </div>
  </section>
</template>
