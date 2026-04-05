<script setup>
import "../assets/chat-window.css";

import { ref, computed } from "vue";
import Message from "./Message.vue";

const props = defineProps({
  currentChannel: {
    type: String,
    required: true,
  },
});

const testMessage = {
  avatarUrl:
    "https://www.cpp.edu/sci/computer-science/img/faculty-staff/zaidi.png",
  user: "Hussain Zaidi",
  text: "Hey",
  time: "1:55PM",
};
const testReply = {
  avatarUrl:
    "https://fortune.com/img-assets/wp-content/uploads/2023/01/OpenAI-Sam-Altman-h_15241239-final.jpg",
  user: "Sam Altman",
  text: "hello",
  time: "1:57PM",
};
</script>

<template>
  <div class="chat-window unselected" style="color: var(--secondary)" v-if="currentChannel == null">
    <p style="margin: 0; font-size: 45px; margin-bottom: 5px">
      <i class="bi bi-chat-right-quote"></i>
    </p>
    <p style="margin: 0; font-size: 20px; width: 250px; text-align: center">
      Select a channel to start the conversation
    </p>
  </div>

  <div class="chat-window" v-if="currentChannel != null">
    <div class="messages">
      <ol class="message-list">
        <li class="message-list-item">
          <div class="date-label">March 19th, 2026</div>
        </li>
        <li class="message-list-item">
          <Message :message="testMessage" :isMe="true" />
        </li>
        <li class="message-list-item">
          <Message :message="testReply" :isMe="false" />
        </li>
      </ol>
    </div>
    <div class="input-area">
      <textarea class="text-input send-message" placeholder="Send a message to Example Text Channel 1..."></textarea>
      <div class="action-button">
        <i class="bi bi-paperclip" style="font-size: 25px"></i>
      </div>
      <div class="action-button" @click="me()">
        <i class="bi bi-send" style="font-size: 25px"></i>
      </div>
    </div>
  </div>
</template>
