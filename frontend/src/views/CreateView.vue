<script setup>
import { ref, inject } from 'vue'

const authorName = inject('userNickname')
const content = ref('')
const selectedFile = ref(null)

const onFileChange = (event) => {
  const files = event.target.files
  if (files && files.length > 0) {
    selectedFile.value = files[0]
  }
}

const handlePublish = () => {
  alert(`Публикуем!\nАвтор: ${authorName.value}\nТекст: ${content.value}\nФайл: ${selectedFile.value ? selectedFile.value.name : 'Нет'}`)
}
</script>

<template>
  <div class="max-w-xl mx-auto py-4">
    <section class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 sm:p-6 shadow-xl">
      <h2 class="text-xl font-bold text-white mb-4 tracking-tight">Создать публикацию</h2>
      
      <form @submit.prevent="handlePublish" class="space-y-4">
        <div>
          <label class="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1">Текст поста</label>
          <textarea 
            v-model="content"
            rows="4"
            placeholder="Поделитесь годным мемом или историей..." 
            class="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-zinc-100 transition-colors resize-none"
          ></textarea>
        </div>

        <div>
          <label class="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1">Прикрепить картинку</label>
          <input 
            type="file"
            accept="image/*"
            @change="onFileChange"
            class="w-full text-xs text-zinc-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-zinc-800 file:text-zinc-300 hover:file:bg-zinc-700 file:cursor-pointer transition-colors"
          />
        </div>

        <button 
          type="submit"
          class="w-full bg-emerald-500 hover:bg-emerald-600 text-zinc-950 font-bold py-2.5 rounded-lg text-sm transition-colors shadow-lg shadow-emerald-500/10 cursor-pointer"
        >
          Опубликовать в ленту
        </button>
      </form>
    </section>
  </div>
</template>
