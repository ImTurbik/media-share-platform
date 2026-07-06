<script setup>
import { inject, onMounted, ref } from 'vue'

const posts = ref([])
const isLoading = ref(true)
const likingPostId = ref(null)
const userNickname = inject('userNickname', ref(''))

const getImageUrl = (imagePath) => {
  if (!imagePath) return ''
  if (/^https?:\/\//i.test(imagePath)) return imagePath
  if (imagePath.startsWith('/')) return `http://localhost:8000${imagePath}`
  return `http://localhost:8000/${imagePath}`
}

const getCurrentNickname = () => userNickname.value?.trim() || ''

const hasLiked = (post) => {
  const currentNickname = getCurrentNickname()
  return Boolean(currentNickname && (post.liked_by || []).includes(currentNickname))
}

const fetchPosts = async () => {
  try {
    isLoading.value = true
    const response = await fetch('http://localhost:8000/api/posts')
    if (!response.ok) {
      throw new Error('Не удалось загрузить ленту')
    }
    const data = await response.json()
    posts.value = data.map((post) => ({
      ...post,
      liked_by: post.liked_by || [],
    }))
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

const handleLike = async (post) => {
  const currentNickname = getCurrentNickname()
  if (!currentNickname || likingPostId.value === post.id) {
    return
  }

  try {
    likingPostId.value = post.id

    const formData = new FormData()
    formData.append('author_name', currentNickname)

    const endpoint = hasLiked(post) ? 'unlike' : 'like'
    const response = await fetch(`http://localhost:8000/api/posts/${post.id}/${endpoint}`, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data?.detail || 'Не удалось изменить лайк')
    }

    post.likes_count = data.likes_count
    post.liked_by = data.liked_by || []
  } catch (error) {
    console.error(error)
    alert(error.message || 'Не удалось изменить лайк')
  } finally {
    likingPostId.value = null
  }
}

onMounted(() => {
  fetchPosts()
})
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
        <span class="text-xs text-zinc-500">{{ new Date(post.created_at).toLocaleDateString() }}</span>
      </div>

      <div v-if="post.content" class="p-4 text-zinc-200 text-sm leading-relaxed whitespace-pre-line">
        {{ post.content }}
      </div>

      <div v-if="post.image_path" class="border-t border-zinc-800 bg-zinc-950 flex justify-center items-center">
        <img :src="getImageUrl(post.image_path)" alt="Картинка" class="w-full h-auto max-h-125 object-contain" />
      </div>

      <div class="px-4 py-2.5 bg-zinc-900/40 border-t border-zinc-800">
        <div class="flex gap-6 text-xs font-bold text-zinc-400 items-center">
          <button
            class="flex items-center gap-1.5 transition-colors cursor-pointer group disabled:cursor-not-allowed"
            :class="hasLiked(post) ? 'text-rose-400' : 'text-zinc-500 hover:text-zinc-300'"
            :disabled="!getCurrentNickname() || likingPostId === post.id"
            @click="handleLike(post)"
          >
            <span>{{ hasLiked(post) ? '❤️' : '💔' }}</span>
            <span>{{ post.likes_count }}</span>
          </button>
          <button class="flex items-center gap-1.5 hover:text-emerald-400 transition-colors cursor-pointer">
            <span>💬</span>
            <span>Комментарии</span>
          </button>
        </div>

        <div v-if="post.liked_by && post.liked_by.length" class="mt-3 flex flex-col gap-2">
          <div class="text-[11px] font-semibold text-zinc-500">
            Уже лайкнули:
          </div>
          <div class="text-xs text-zinc-200 leading-relaxed">
            <template v-for="(nickname, index) in post.liked_by" :key="`${post.id}-${nickname}`">
              <span>@{{ nickname }}</span><span v-if="index < post.liked_by.length - 1">, </span>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
