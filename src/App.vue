<template>
  <NavBar />
  <main class="content">
    <router-view />
  </main>
</template>

<script setup lang="ts">
import NavBar from './components/NavBar.vue'
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

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  overflow-x: hidden;
}

body {
  margin: 0;
  min-height: 100vh;
  overflow-x: hidden;
  background-color: rgb(40, 70, 150);
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
