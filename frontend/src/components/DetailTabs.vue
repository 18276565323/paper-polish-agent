<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  result: {
    type: Object,
    default: null,
  },
})

const tabs = [
  { key: 'modify_detail', label: '修改明细' },
  { key: 'remaining_problem', label: '剩余问题' },
  { key: 'ai_learning_knowledge', label: 'AI 知识点' },
  { key: 'practical_operation_points', label: '实操要点' },
  { key: 'project_resume_highlight', label: '简历亮点' },
]

const activeKey = ref(tabs[0].key)

const activeContent = computed(() => {
  if (!props.result) return '暂无结构化结果'
  return props.result[activeKey.value] || '暂无内容'
})
</script>

<template>
  <section class="detail-band">
    <div class="tabs" role="tablist">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        type="button"
        :class="{ active: activeKey === tab.key }"
        @click="activeKey = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>
    <div class="detail-content">
      <p>{{ activeContent }}</p>
    </div>
  </section>
</template>
