<script setup>
import { inject, onMounted, reactive, ref } from 'vue'
import { API_BASE_URL } from '@/config'

const posts = ref([])
const isLoading = ref(true)
const likingPostId = ref(null)
const commentingPostId = ref(null)
const deletingCommentId = ref(null)
const openCommentsPostId = ref(null)
const userNickname = inject('userNickname', ref(''))
const commentTexts = reactive({})

const getImageUrl = (imagePath) => {
  if (!imagePath) return ''
  if (/^https?:\/\//i.test(imagePath)) return imagePath
  if (imagePath.startsWith('/')) return `${API_BASE_URL}${imagePath}`
  return `${API_BASE_URL}/${imagePath}`
}

const getCurrentNickname = () => userNickname.value?.trim() || ''

const hasLiked = (post) => {
  const currentNickname = getCurrentNickname()
  return Boolean(currentNickname && (post.liked_by || []).includes(currentNickname))
}

const normalizePost = (post) => ({
  ...post,
  liked_by: post.liked_by || [],
  comments: post.comments || [],
})

const fetchPosts = async () => {
  try {
    isLoading.value = true
    const response = await fetch(`${API_BASE_URL}/api/posts`)
    if (!response.ok) {
      throw new Error('Не удалось загрузить ленту')
    }
    const data = await response.json()
    posts.value = data.map(normalizePost)
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
    const response = await fetch(`${API_BASE_URL}/api/posts/${post.id}/${endpoint}`, {
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

const handleAddComment = async (post) => {
  const currentNickname = getCurrentNickname()
  const text = (commentTexts[post.id] || '').trim()

  if (!currentNickname || !text || commentingPostId.value === post.id) {
    return
  }

  try {
    commentingPostId.value = post.id

    const formData = new FormData()
    formData.append('author_name', currentNickname)
    formData.append('text', text)

    const response = await fetch(`${API_BASE_URL}/api/posts/${post.id}/comments`, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data?.detail || 'Не удалось добавить комментарий')
    }

    post.comments = [...post.comments, data.comment]
    commentTexts[post.id] = ''
  } catch (error) {
    console.error(error)
    alert(error.message || 'Не удалось добавить комментарий')
  } finally {
    commentingPostId.value = null
  }
}

const handleDeleteComment = async (post, comment) => {
  const currentNickname = getCurrentNickname()
  if (!currentNickname || currentNickname !== comment.author_name || deletingCommentId.value === comment.id) {
    return
  }

  try {
    deletingCommentId.value = comment.id

    const response = await fetch(
      `${API_BASE_URL}/api/posts/${post.id}/comments/${comment.id}?author_name=${encodeURIComponent(currentNickname)}`,
      {
        method: 'DELETE',
      },
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data?.detail || 'Не удалось удалить комментарий')
    }

    post.comments = post.comments.filter((item) => item.id !== comment.id)
  } catch (error) {
    console.error(error)
    alert(error.message || 'Не удалось удалить комментарий')
  } finally {
    deletingCommentId.value = null
  }
}

const toggleComments = (postId) => {
  openCommentsPostId.value = openCommentsPostId.value === postId ? null : postId
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <div class="max-w-xl mx-auto space-y-6">
    <!-- <h3 class="text-xl font-black text-white tracking-tight px-1">
      А это лента публикаций :>
    </h3> -->

    <div class="flex justify-center">
      <button @click="fetchPosts" class="inline-flex items-center justify-center rounded-lg bg-zinc-800 px-4 py-2 text-sm font-semibold text-zinc-100 shadow-md shadow-black/20 transition-colors hover:bg-zinc-700 active:bg-zinc-600 ">
        Обновить ленту
      </button>
    </div>

    <div 
      v-for="post in posts" 
      :key="post.id" 
      class="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden shadow-lg"
    >
      <div class="px-4 py-3 bg-zinc-900/50 border-b border-zinc-800 flex justify-between items-center">
        <span class="font-bold text-emerald-400 text-sm">@{{ post.author_name }}</span>
        <span class="text-xs text-zinc-500">{{ 
        new Date(post.created_at + 'Z').toLocaleDateString('ru-RU', {
          timeZone: 'Europe/Moscow',
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
          })
        }}</span>
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
          <button
            class="flex items-center gap-1.5 transition-colors cursor-pointer"
            :class="openCommentsPostId === post.id ? 'text-emerald-400' : 'hover:text-emerald-400'"
            @click="toggleComments(post.id)"
          >
            <span>💬</span>
            <span>
              Комментарии
              <template v-if="post.comments && post.comments.length">
                ({{ post.comments.length }})
              </template>
            </span>
          </button>
        </div>

        <div v-if="openCommentsPostId === post.id" class="mt-3 space-y-3">
          <form class="space-y-2" @submit.prevent="handleAddComment(post)">
            <textarea
              v-model="commentTexts[post.id]"
              rows="2"
              placeholder="Комментарий..."
              class="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-zinc-100 transition-colors resize-none"
            ></textarea>
            <button
              type="submit"
              :disabled="!getCurrentNickname() || commentingPostId === post.id"
              class="bg-zinc-800 hover:bg-zinc-700 disabled:bg-zinc-800 disabled:text-zinc-500 text-zinc-100 font-semibold px-3 py-1.5 rounded-lg text-xs transition-colors cursor-pointer disabled:cursor-not-allowed"
            >
              {{ commentingPostId === post.id ? 'Отправка...' : 'Добавить комментарий' }}
            </button>
          </form>

          <div v-if="post.comments && post.comments.length" class="space-y-2">
            <div
              v-for="comment in post.comments"
              :key="comment.id"
              class="bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2"
            >
              <div class="flex justify-between gap-2 text-xs text-zinc-500">
                <span>@{{ comment.author_name }}</span>
                <button
                  v-if="comment.author_name === getCurrentNickname()"
                  class="text-zinc-500 hover:text-rose-400 transition-colors cursor-pointer disabled:cursor-not-allowed"
                  :disabled="deletingCommentId === comment.id"
                  @click="handleDeleteComment(post, comment)"
                >
                  Удалить
                </button>
              </div>
              <div class="mt-1 text-sm text-zinc-200 whitespace-pre-line">
                {{ comment.text }}
              </div>
            </div>
          </div>
          <div v-else class="text-xs text-zinc-500">
            Комментариев пока нет
          </div>
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
