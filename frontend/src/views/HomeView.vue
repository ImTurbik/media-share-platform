<script setup>
import { ref } from 'vue'

const posts = ref([
  {
    id: 1,
    author_name: "author1",
    content: "Осторожно! Здесь бывает экстремистский юмор...",
    image_path: "https://cdn.discordapp.com/attachments/833789145260359691/1522591228686766251/image.png?ex=6a4baa15&is=6a4a5895&hm=c79342ac400cefe28acf07cc612c36f95799bc7e04544a3c9ca68177feb33ca3&",
    likes_count: 228,
    created_at: "15 минут назад"
  },
  {
    id: 2,
    author_name: "author2",
    content: null,
    image_path: "https://cdn.discordapp.com/attachments/833789145260359691/1522591254221950976/image.png?ex=6a4baa1b&is=6a4a589b&hm=1561d380179e1f5fbdddf5114f452669b25039913614fc59c710d4c8a7ba09df&",
    likes_count: 123,
    created_at: "2 часа назад"
  }
])
</script>

<template>
  <div class="max-w-xl mx-auto space-y-6">
    <h3 class="text-xl font-black text-white tracking-tight px-1">
      А это лента публикаций :>
    </h3>
    
    <div 
      v-for="post in posts" 
      :key="post.id" 
      class="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden shadow-lg"
    >
      <div class="px-4 py-3 bg-zinc-900/50 border-b border-zinc-800 flex justify-between items-center">
        <span class="font-bold text-emerald-400 text-sm">@{{ post.author_name }}</span>
        <span class="text-xs text-zinc-500">{{ post.created_at }}</span>
      </div>
      
      <div v-if="post.content" class="p-4 text-zinc-200 text-sm leading-relaxed whitespace-pre-line">
        {{ post.content }}
      </div>
      
      <div v-if="post.image_path" class="border-t border-zinc-800 bg-zinc-950 flex justify-center items-center">
        <img :src="post.image_path" alt="Мем" class="w-full h-auto max-h-125 object-contain" />
      </div>
      
      <div class="px-4 py-2.5 bg-zinc-900/40 border-t border-zinc-800 flex gap-6 text-xs font-bold text-zinc-400">
        <button class="flex items-center gap-1.5 hover:text-rose-400 transition-colors cursor-pointer group">
          <span>❤️</span> <span>{{ post.likes_count }}</span>
        </button>
        <button class="flex items-center gap-1.5 hover:text-emerald-400 transition-colors cursor-pointer">
          <span>💬</span> <span>Комментарии</span>
        </button>
      </div>
    </div>
  </div>
</template>
