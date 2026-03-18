<script setup>
import ServerBar from "./components/ServerBar.vue";
import ChannelBar from "./components/ChannelBar.vue";
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
      <div class="server-sidebar">
        <ServerBar />
      </div>
      <div class="left-sidebar">
        <ChannelBar />
      </div>
      <div class="main-content">
        <ChatWindow />
      </div>
      <div class="right-sidebar">
        <p style="margin: 0; font-weight: 700;">Members</p>
      </div>
    </div>
  </div>
</template>
