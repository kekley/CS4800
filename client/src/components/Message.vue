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
console.log("Message component received message:", props.message);
import "../assets/chat-message.css";

</script>

<template>
  <div :class="['chat-message', { me: isMe }]">
    <div class="container">
      <img class="avatar" :src="message.author.avatar_url" />
      <div class="vertical">
        <div class="header">
          <span class="username">{{ message.author.username }}</span>
          <span class="timestamp">{{ message.created_at }}</span>
        </div>
        <div class="contents">
          <div v-if="message.imageUrl" class="attachment-image">
            <img :src="message.imageUrl" alt="Sent Image" />
          </div>
          <span v-if="message.content" class="message-text">{{
            message.content
          }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
