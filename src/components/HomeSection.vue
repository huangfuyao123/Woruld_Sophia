<template>
  <div class="hero">
    <h1 class="title">NetClub</h1>
    <p class="intro">
      Amidst the relentless iteration of technology
      <br />
      and thought, collaboration remains timeless. Woruld Sophia bridges the
      <br />
      realm where managers and creators co-exist and co-create.
    </p>
  </div>
</template>

<style scoped>
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 50px);
  padding: 24px;
}

.title {
  font-size: clamp(36px, 10vw, 160px);
  color: #fff;
  font-family: 'JuliaMono BlackItalic';
  text-align: center;
  line-height: 1.1;
  margin: 0;
  word-break: break-word;
  text-shadow:
    0 0 10px #fff,
    0 0 30px #0ff,
    0 0 60px #00f,
    0 0 100px #00f;
}

.intro {
  font-size: clamp(12px, 2.5vw, 20px);
  color: #fff;
  font-family: 'JuliaMono BlackItalic';
  text-align: center;
  margin-top: 12px;
  line-height: 1.6;
  text-shadow:
    0 0 10px #fff,
    0 0 30px #0ff,
    0 0 60px #00f,
    0 0 100px #00f;
}

@media (max-width: 768px) {
  .hero {
    padding: 16px;
  }

  .title {
    text-shadow:
      0 0 8px #fff,
      0 0 24px #0ff,
      0 0 48px #00f;
  }

  .intro {
    text-shadow:
      0 0 8px #fff,
      0 0 24px #0ff,
      0 0 48px #00f;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: clamp(36px, 14vw, 60px);
    text-shadow:
      0 0 6px #fff,
      0 0 16px #0ff,
      0 0 32px #00f;
  }

  .intro {
    font-size: clamp(12px, 4vw, 16px);
    text-shadow:
      0 0 6px #fff,
      0 0 16px #0ff,
      0 0 32px #00f;
  }
}
</style>
