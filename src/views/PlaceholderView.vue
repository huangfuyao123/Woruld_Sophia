<template>
  <section class="placeholder">
    <h1 class="title">{{ title }}</h1>
    <p class="hint">该版块正在建设中，敬请期待。</p>
    <RouterLink class="back" to="/">返回首页</RouterLink>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'

const route = useRoute()
const title = computed(() => (route.meta.title as string) ?? '建设中')
</script>

<style scoped>
.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 50px);
  padding: 24px;
  color: #fff;
  text-align: center;
}

.title {
  font-size: clamp(32px, 8vw, 96px);
  font-family: 'JuliaMono BlackItalic';
  margin: 0;
  text-shadow:
    0 0 10px #fff,
    0 0 30px #0ff,
    0 0 60px #00f;
}

.hint {
  margin-top: 12px;
  font-size: clamp(12px, 2.5vw, 18px);
  font-family: '寒蝉正楷体';
  opacity: 0.85;
}

.back {
  margin-top: 24px;
  padding: 8px 20px;
  border: 2px solid #fff;
  border-radius: 8px;
  color: #fff;
  text-decoration: none;
  font-family: 'JuliaMono Medium';
  transition: 0.2s;
}

.back:hover {
  background: rgba(255, 255, 255, 0.15);
}

@media (max-width: 768px) {
  .placeholder {
    padding: 16px;
  }

  .title {
    text-shadow:
      0 0 8px #fff,
      0 0 24px #0ff,
      0 0 48px #00f;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: clamp(28px, 10vw, 48px);
    text-shadow:
      0 0 6px #fff,
      0 0 16px #0ff,
      0 0 32px #00f;
  }

  .hint {
    font-size: clamp(12px, 3.5vw, 16px);
  }

  .back {
    margin-top: 20px;
    padding: 7px 18px;
    font-size: 14px;
  }
}
</style>
