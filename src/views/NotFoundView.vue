<template>
  <section class="not-found">
    <h1 class="code">404</h1>
    <p class="text">页面不存在</p>
    <RouterLink class="back" to="/">返回首页</RouterLink>
  </section>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 50px);
  color: #fff;
  text-align: center;
}

.code {
  font-size: clamp(56px, 18vw, 200px);
  font-family: 'JuliaMono BlackItalic';
  margin: 0;
  line-height: 1;
  text-shadow:
    0 0 10px #fff,
    0 0 30px #0ff,
    0 0 60px #00f;
}

.text {
  margin-top: 8px;
  font-size: clamp(14px, 3vw, 22px);
  font-family: '寒蝉正楷体';
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

@media (max-width: 480px) {
  .code {
    font-size: clamp(48px, 20vw, 96px);
    text-shadow:
      0 0 8px #fff,
      0 0 20px #0ff,
      0 0 40px #00f;
  }

  .text {
    font-size: clamp(13px, 4vw, 18px);
  }

  .back {
    margin-top: 20px;
    padding: 8px 18px;
    font-size: 14px;
  }
}
</style>
