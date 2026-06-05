<script setup>
const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  requirement: {
    type: String,
    required: true,
  },
  busy: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:text', 'update:requirement', 'submit'])

const requirements = [
  '综合润色',
  '学术化润色',
  '逻辑优化',
  '合规降重',
  '格式校对',
  '中英双语精修',
]
</script>

<template>
  <section class="panel input-panel">
    <div class="panel-heading">
      <div>
        <p class="eyebrow">Input</p>
        <h2>论文原文</h2>
      </div>
      <span class="counter">{{ props.text.length }} 字</span>
    </div>

    <textarea
      class="paper-input"
      :value="props.text"
      placeholder="粘贴需要润色的论文段落..."
      @input="emit('update:text', $event.target.value)"
    ></textarea>

    <div class="form-row">
      <label>
        <span>润色需求</span>
        <select
          :value="props.requirement"
          @change="emit('update:requirement', $event.target.value)"
        >
          <option v-for="item in requirements" :key="item" :value="item">
            {{ item }}
          </option>
        </select>
      </label>
      <button
        class="primary-action"
        type="button"
        :disabled="busy || !props.text.trim()"
        @click="emit('submit')"
      >
        {{ busy ? '润色中...' : '开始润色' }}
      </button>
    </div>
  </section>
</template>
