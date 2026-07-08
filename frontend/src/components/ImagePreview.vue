<script setup>
import { ref } from 'vue'

defineProps({
  alt: {
    type: String,
    default: 'Изображение',
  },
  src: {
    type: String,
    required: true,
  },
})

const isOpen = ref(false)

const openImage = () => {
  isOpen.value = true
}

const closeImage = () => {
  isOpen.value = false
}
</script>

<template>
  <div class="w-full">
    <img
      :src="src"
      :alt="alt"
      class="w-full h-auto max-h-125 object-contain cursor-zoom-in transition-opacity hover:opacity-90"
      @click="openImage"
    />

    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4"
      @click.self="closeImage"
    >
      <button
        type="button"
        class="absolute right-4 top-4 text-sm font-semibold text-zinc-300 hover:text-white"
        @click="closeImage"
      >
        Закрыть
      </button>
      <img
        :src="src"
        :alt="alt"
        class="max-h-[90vh] max-w-[92vw] rounded-xl object-contain shadow-2xl"
        @click.stop
      />
    </div>
  </div>
</template>
