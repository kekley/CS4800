<script setup>
const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  isMe: {
    type: Boolean,
    default: false,
  },
});
import "../assets/chat-message.css";


console.log(JSON.stringify(props));
</script>

<template>
  <div :class="['chat-message', { me: isMe }]">
    <div class="container">
      <img class="avatar" :src="message.avatarUrl" />
      <div class="vertical">
        <div class="header">
          <span class="username">{{ message.user }}</span>
          <span class="timestamp">{{ message.time }}</span>
        </div>
        <div class="contents">
          <div v-if="message.imageUrl" class="attachment-image">
            <img :src="message.imageUrl" alt="Sent Image" />
          </div>
          <span v-if="message.text" class="message-text">{{
            message.text
          }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
