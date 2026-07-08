<script setup>
import { inject, onMounted, ref, watch } from 'vue'
import { API_BASE_URL } from '@/config'
import ImagePreview from '@/components/ImagePreview.vue'

const userNickname = inject('userNickname', ref(''))
const profilePosts = ref([])
const isLoading = ref(true)
const deletingPostId = ref(null)

const getCurrentNickname = () => userNickname.value?.trim() || ''

const fetchPosts = async () => {
  const currentNickname = userNickname.value?.trim()
  if (!currentNickname) {
    profilePosts.value = []
    isLoading.value = false
    return
  }

  try {
    isLoading.value = true
    const response = await fetch(`${API_BASE_URL}/api/users/${encodeURIComponent(currentNickname)}/posts`)
    if (!response.ok) {
      throw new Error('Не удалось загрузить профиль')
    }
    profilePosts.value = await response.json()
  } catch (error) {
    console.error(error)
    profilePosts.value = []
  } finally {
    isLoading.value = false
  }
}

const handleDeletePost = async (post) => {
  const currentNickname = getCurrentNickname()
  if (!currentNickname || deletingPostId.value === post.id) {
    return
  }

  try {
    deletingPostId.value = post.id
    const response = await fetch(
      `${API_BASE_URL}/api/posts/${post.id}?author_name=${encodeURIComponent(currentNickname)}`,
      {
        method: 'DELETE',
      },
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data?.detail || 'Не удалось удалить пост')
    }

    profilePosts.value = profilePosts.value.filter((item) => item.id !== post.id)
  } catch (error) {
    console.error(error)
    alert(error.message || 'Не удалось удалить пост')
  } finally {
    deletingPostId.value = null
  }
}

onMounted(fetchPosts)

watch(
  () => userNickname.value,
  () => {
    fetchPosts()
  },
)
</script>

<template>
  <div class="max-w-xl mx-auto space-y-6">
    <div class="space-y-1">
      <h1 class="text-xl font-black text-white tracking-tight">Профиль</h1>
      <p class="text-sm text-zinc-400">
        <span v-if="userNickname">Посты пользователя @{{ userNickname }}</span>
        <span v-else>Сначала нужно указать ник</span>
      </p>
    </div>

    <div v-if="isLoading" class="text-sm text-zinc-400">
      Загрузка...
    </div>

    <div v-else-if="profilePosts.length" class="space-y-6">
      <article
        v-for="post in profilePosts"
        :key="post.id"
        class="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden shadow-lg"
      >
        <div class="px-4 py-3 bg-zinc-900/50 border-b border-zinc-800 flex justify-between items-center">
          <span class="font-bold text-emerald-400 text-sm">@{{ post.author_name }}</span>
          <span class="text-xs text-zinc-500">
            {{
              new Date(post.created_at + 'Z').toLocaleDateString('ru-RU', {
                timeZone: 'Europe/Moscow',
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
              })
            }}
          </span>
        </div>

        <div v-if="post.content" class="p-4 text-zinc-200 text-sm leading-relaxed whitespace-pre-line">
          {{ post.content }}
        </div>

        <div v-if="post.image_path" class="border-t border-zinc-800 bg-zinc-950 flex justify-center items-center">
          <ImagePreview :src="`${API_BASE_URL}${post.image_path}`" alt="Картинка" />
        </div>

        <div class="px-4 py-2.5 bg-zinc-900/40 border-t border-zinc-800 flex items-center justify-between gap-3 text-xs text-zinc-400">
          <div>
            Лайков: {{ post.likes_count }} | Комментариев: {{ post.comments?.length || 0 }}
          </div>
          <button
            v-if="post.author_name === getCurrentNickname()"
            class="text-rose-400 hover:text-rose-300 transition-colors cursor-pointer disabled:cursor-not-allowed"
            :disabled="deletingPostId === post.id"
            @click="handleDeletePost(post)"
          >
            {{ deletingPostId === post.id ? 'Удаление...' : 'Удалить пост' }}
          </button>
        </div>
      </article>
    </div>

    <div v-else class="text-sm text-zinc-500">
      У этого ника пока нет публикаций.
    </div>
  </div>
</template>
