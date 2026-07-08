<script setup>
import { computed, inject, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { API_BASE_URL } from '@/config'
import ImagePreview from '@/components/ImagePreview.vue'

const route = useRoute()
const userNickname = inject('userNickname', ref(''))
const post = ref(null)
const isLoading = ref(true)
const likingPost = ref(false)
const commentingPost = ref(false)
const deletingCommentId = ref(null)
const openComments = ref(false)
const commentText = ref('')
const errorMessage = ref('')

const getCurrentNickname = () => userNickname.value?.trim() || ''

const postId = computed(() => Number(route.params.postId))

const hasLiked = () => {
  const currentNickname = getCurrentNickname()
  return Boolean(currentNickname && post.value && (post.value.liked_by || []).includes(currentNickname))
}

const normalizePost = (data) => ({
  ...data,
  liked_by: data.liked_by || [],
  comments: data.comments || [],
})

const fetchPost = async () => {
  try {
    isLoading.value = true
    errorMessage.value = ''
    const response = await fetch(`${API_BASE_URL}/api/posts/${postId.value}`)
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data?.detail || 'Не удалось загрузить пост')
    }

    post.value = normalizePost(data)
  } catch (error) {
    console.error(error)
    post.value = null
    errorMessage.value = error.message || 'Не удалось загрузить пост'
  } finally {
    isLoading.value = false
  }
}

const handleLike = async () => {
  const currentNickname = getCurrentNickname()
  if (!currentNickname || !post.value || likingPost.value) {
    return
  }

  try {
    likingPost.value = true

    const formData = new FormData()
    formData.append('author_name', currentNickname)

    const endpoint = hasLiked() ? 'unlike' : 'like'
    const response = await fetch(`${API_BASE_URL}/api/posts/${post.value.id}/${endpoint}`, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data?.detail || 'Не удалось изменить лайк')
    }

    post.value.likes_count = data.likes_count
    post.value.liked_by = data.liked_by || []
  } catch (error) {
    console.error(error)
    alert(error.message || 'Не удалось изменить лайк')
  } finally {
    likingPost.value = false
  }
}

const handleAddComment = async () => {
  const currentNickname = getCurrentNickname()
  const text = commentText.value.trim()

  if (!currentNickname || !post.value || !text || commentingPost.value) {
    return
  }

  try {
    commentingPost.value = true

    const formData = new FormData()
    formData.append('author_name', currentNickname)
    formData.append('text', text)

    const response = await fetch(`${API_BASE_URL}/api/posts/${post.value.id}/comments`, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data?.detail || 'Не удалось добавить комментарий')
    }

    post.value.comments = [...post.value.comments, data.comment]
    commentText.value = ''
  } catch (error) {
    console.error(error)
    alert(error.message || 'Не удалось добавить комментарий')
  } finally {
    commentingPost.value = false
  }
}

const handleDeleteComment = async (comment) => {
  const currentNickname = getCurrentNickname()
  if (!currentNickname || currentNickname !== comment.author_name || deletingCommentId.value === comment.id) {
    return
  }

  try {
    deletingCommentId.value = comment.id

    const response = await fetch(
      `${API_BASE_URL}/api/posts/${post.value.id}/comments/${comment.id}?author_name=${encodeURIComponent(currentNickname)}`,
      {
        method: 'DELETE',
      },
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data?.detail || 'Не удалось удалить комментарий')
    }

    post.value.comments = post.value.comments.filter((item) => item.id !== comment.id)
  } catch (error) {
    console.error(error)
    alert(error.message || 'Не удалось удалить комментарий')
  } finally {
    deletingCommentId.value = null
  }
}

onMounted(fetchPost)
watch(postId, fetchPost)
</script>

<template>
  <div class="max-w-xl mx-auto space-y-6">
    <div v-if="isLoading" class="text-sm text-zinc-400">
      Загрузка...
    </div>

    <div v-else-if="errorMessage" class="text-sm text-rose-400">
      {{ errorMessage }}
    </div>

    <article v-else-if="post" class="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden shadow-lg">
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

      <div class="px-4 py-2.5 bg-zinc-900/40 border-t border-zinc-800">
        <div class="flex gap-6 text-xs font-bold text-zinc-400 items-center">
          <button
            class="flex items-center gap-1.5 transition-colors cursor-pointer group disabled:cursor-not-allowed"
            :class="hasLiked() ? 'text-rose-400' : 'text-zinc-500 hover:text-zinc-300'"
            :disabled="!getCurrentNickname() || likingPost"
            @click="handleLike"
          >
            <span>{{ hasLiked() ? '❤️' : '💔' }}</span>
            <span>{{ post.likes_count }}</span>
          </button>
          <button
            class="flex items-center gap-1.5 transition-colors cursor-pointer"
            :class="openComments ? 'text-emerald-400' : 'hover:text-emerald-400'"
            @click="openComments = !openComments"
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

        <div v-if="openComments" class="mt-3 space-y-3">
          <form class="space-y-2" @submit.prevent="handleAddComment">
            <textarea
              v-model="commentText"
              rows="2"
              placeholder="Комментарий..."
              class="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-zinc-100 transition-colors resize-none"
            ></textarea>
            <button
              type="submit"
              :disabled="!getCurrentNickname() || commentingPost"
              class="bg-zinc-800 hover:bg-zinc-700 disabled:bg-zinc-800 disabled:text-zinc-500 text-zinc-100 font-semibold px-3 py-1.5 rounded-lg text-xs transition-colors cursor-pointer disabled:cursor-not-allowed"
            >
              {{ commentingPost ? 'Отправка...' : 'Добавить комментарий' }}
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
                  @click="handleDeleteComment(comment)"
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
    </article>
  </div>
</template>
