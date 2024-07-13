<template>
  <div id="app">
    <VoiceTranslator />
  </div>
</template>

<script>
import VoiceTranslator from './components/VoiceTranslator.vue';

export default {
  name: 'App',
  components: {
    VoiceTranslator
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
