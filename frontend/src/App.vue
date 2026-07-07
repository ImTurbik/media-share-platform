<script setup>
import { RouterView, RouterLink } from 'vue-router';
import { ref, onMounted, provide } from 'vue';

const userNickname = ref('');
const showModal = ref(false);
const inputNickname = ref('');

onMounted(() => {
  const savedNickname = localStorage.getItem('user_nickname')
  if (savedNickname) {
    userNickname.value = savedNickname
  } else {
    showModal.value = true
  }
})

const saveNickname = () => {
  if (inputNickname.value.trim()) {
    const cleanNick = inputNickname.value.trim()
    localStorage.setItem('user_nickname', cleanNick)
    userNickname.value = cleanNick
    showModal.value = false
  }
}

provide('userNickname', userNickname)

const changeNickname = () => {
  inputNickname.value = userNickname.value
  showModal.value = true
}

</script>

<template>
  <div class="flex flex-col min-h-screen bg-zinc-950 text-zinc-100 font-sans">
    
    <header class="bg-zinc-900 border-b border-zinc-800 py-4 sticky top-0 z-50">
      <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
        <RouterLink to="/" class="text-2xl font-black text-emerald-400 tracking-tight">
          МемХостинг
        </RouterLink>
        <nav class="flex gap-6">
          <RouterLink to="/" class="nav-link text-zinc-400 hover:text-emerald-400 font-medium transition-colors">
            Лента
          </RouterLink>
          <RouterLink to="/create" class="nav-link text-zinc-400 hover:text-emerald-400 font-medium transition-colors">
            Создать пост
          </RouterLink>
          <RouterLink to="/about" class="nav-link text-zinc-400 hover:text-emerald-400 font-medium transition-colors">
            О проекте
          </RouterLink>

          <!-- КНОПКА ПЕРЕПРАВКИ НА СТРАНИЦУ ПРОФИЛЯ -->
          <RouterLink to="/profile" class="border-l border-zinc-800 pl-4 nav-link text-zinc-400 hover:text-emerald-400 font-medium transition-colors">
            Профиль
          </RouterLink>

          <!-- КНОПКА СМЕНЫ НИКА -->
          <button
            @click="changeNickname"
            class="flex items-center gap-1.5 text-zinc-400 hover:text-emerald-400 font-medium transition-colors text-sm cursor-pointer"
          >
            <span>@{{ userNickname }}</span>
            <span class="text-xs opacity-60">✏️</span>
          </button>

        </nav>
      </div>
    </header>

    <main class="grow max-w-2xl mx-auto w-full px-4 py-8">
      <RouterView />
    </main>


    <!-- МОДАЛЬНОЕ ОКНО ВВОДА НИКА -->
    <div v-if="showModal" class="fixed inset-0 z-100 flex items-center justify-center bg-black/60 backdrop-blur-md p-4">
      <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 max-w-sm w-full shadow-2xl space-y-4">
        <div class="text-center">
          <h3 class="text-lg font-black text-white tracking-tight">Добро пожаловать!</h3>
          <p class="text-xs text-zinc-400 mt-1">Введите ваш никнейм для публикации мемов и комментариев</p>
        </div>
        
        <form @submit.prevent="saveNickname" class="space-y-3">
          <input 
            v-model="inputNickname"
            type="text" 
            required
            class="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-zinc-100 transition-colors text-center font-semibold"
          />
          <button 
            type="submit" 
            class="w-full bg-emerald-500 hover:bg-emerald-600 text-zinc-950 font-bold py-2 rounded-lg text-sm transition-colors cursor-pointer"
          >
            Сохранить и войти
          </button>
        </form>
      </div>
    </div>


    <footer class="bg-zinc-900 border-t border-zinc-800 py-4 mt-auto">
      <div class="max-w-4xl mx-auto px-4 text-center text-xs text-zinc-500 font-medium tracking-wide">
        Made with love ❤️ by 
        <a 
          href="https://github.com/ImTurbik"
          target="_blank"
          class="text-zinc-400 hover:text-emerald-400 decoration-zinc-700 hover:decoration-emerald-400 transition-all"
        >
          Me
        </a>
      </div>
    </footer>

  </div>
</template>

<style scoped>
  .nav-link.router-link-active {
    color: #34d399;
  }
</style>