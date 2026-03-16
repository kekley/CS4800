<script setup>
import ChatWindow from "./components/ChatWindow.vue";
import { ref, computed } from "vue";
</script>
<style>
body {
  margin: 0;
}
</style>

<template>
  <div class="main">
    <div class="top-bar">Title Bar</div>
    <div class="app-window">
      <div class="left-sidebar"></div>
      <div class="main-content">
        <ChatWindow />
      </div>
      <div class="right-sidebar"></div>
    </div>
  </div>
</template>
