<template>
  <NavBar v-if="isHomePage" />
  <main class="content">
    <router-view />
  </main>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'

const route = useRoute()
const isHomePage = computed(() => route.name === 'home')
</script>

<style>
@font-face {
  font-family: 'JuliaMono BlackItalic';
  src: url('/fonts/JuliaMono-BlackItalic.ttf') format('truetype');
}
@font-face {
  font-family: '寒蝉正楷体';
  src: url('/fonts/寒蝉正楷体.ttf') format('truetype');
}
@font-face {
  font-family: 'JuliaMono Medium';
  src: url('/fonts/JuliaMono-Medium.ttf') format('truetype');
}

:root {
  font-size: 16px;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  overflow-x: hidden;
  -webkit-text-size-adjust: 100%;
}

@media (max-width: 768px) {
  :root {
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  :root {
    font-size: 14px;
  }
}

body {
  margin: 0;
  min-height: 100vh;
  overflow-x: hidden;
  background-color: rgb(40, 70, 150);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  min-height: 100vh;
}

.content {
  width: 100%;
  min-height: 100vh;
  background-color: rgb(40, 70, 150);
  padding-top: 0;
}
</style>
