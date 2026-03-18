<script setup>
import "../assets/channel-bar.css";

import { ref, computed } from "vue";

let channels = [
  {
    "name": "Example Text Channel 1",
    "channelId": 10
  },
  {
    "name": "Example Text Channel 2",
    "channelId": 10
  }
]

</script>

<template>
  <div class="channel-bar">
    <p class="label">Chat Channels</p>
    <template v-for="channel in channels">
      <div class="channel-thumb">
        <span style="font-weight: 700;"><i class="bi bi-hash"></i> {{ channel.name }}</span> <br>
        <div class="presence-indicator">
          <div class="spinner-grow text-success" role="status"></div>
          <p>5 members here</p>
        </div>
      </div>
    </template>
    <p class="label">Voice Channels</p>
  </div>
</template>
