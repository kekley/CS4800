<script setup>
import "../assets/channel-bar.css";
import { watch, ref } from "vue";

const props = defineProps({
  currentServer: {
    type: String,
    required: true,
  },
  currentChannel: {
    type: String,
    required: true,
  }
});
const emit = defineEmits(['update-currentChannel']);

let loading = ref(false);
let chatChannels = [
  {
    "name": "Example Text Channel 1",
    "channelId": 10
  },
  {
    "name": "Example Text Channel 2",
    "channelId": 11
  }
];
let voiceChannels = [];

watch(() => props.currentServer, (newServer) => {
  loadChannelData(newServer);
});

const loadChannelData = async (server) => {
  if (server != 'home') {
    loading.value = true;
    setTimeout(() => {
      loading.value = false;
    }, 1000);
  }
}

const selectChannel = (channelId) => {
  emit('update-currentChannel', channelId);
}

</script>

<template>
  <div class="channel-bar working" v-if="loading">
    <div class="spinner-border custom-spinner" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <div class="channel-bar" v-if="!loading">
    <div v-if="currentServer == 'home'">
      <p class="label">Your Invites</p>
    </div>

    <div v-if="currentServer != 'home'">
      <p class="label">Chat Channels</p>
      <template v-for="channel in chatChannels">
        <div :class="{'channel-thumb': true, 'active': (currentChannel == channel.channelId)}" @click="selectChannel(channel.channelId)">
          <span style="font-weight: 700;"><i class="bi bi-hash"></i> {{ channel.name }}</span> <br>
          <div class="presence-indicator" v-if="channel.channelId == 10">
            <div class="spinner-grow text-success" role="status"></div>
            <p>5 members here</p>
          </div>
        </div>
      </template>
      <p class="label">Voice Channels</p>
    </div>
  </div>
</template>
