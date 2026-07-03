<script setup>
  import { RouterView, RouterLink } from 'vue-router';
</script>

<template>
  <div class="min-h-screen bg-zinc-950 text-zinc-100 font-sans">
    
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
        </nav>
      </div>
    </header>

    <main class="max-w-2xl mx-auto px-4 py-8">
      <RouterView />
    </main>

  </div>
</template>

<style scoped>
  .nav-link.router-link-active {
    color: #34d399;
  }
</style>