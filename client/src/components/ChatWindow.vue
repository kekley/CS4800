<script setup>
import "../assets/chat-window.css";

import { ref, computed } from "vue";
import Message from "./Message.vue";

const testMessage = {
  avatarUrl:
    "https://www.cpp.edu/sci/computer-science/img/faculty-staff/zaidi.png",
  user: "Hussain Zaidi",
  text: "Hey",
  time: "1:55PM",
};
const testReply= {
  avatarUrl:
    "https://fortune.com/img-assets/wp-content/uploads/2023/01/OpenAI-Sam-Altman-h_15241239-final.jpg",
  user: "Freak Ass Altman",
  text: "kill yourself",
  time: "1:57PM",
};

</script>

<template>
  <div class="chat-window">
    <div class="messages">
      <ol class="message-list">
        <li class="message-list-item">
          <Message :message="testMessage" :isMe="true" />
        </li>
        <li class="message-list-item">
          <Message :message="testReply" :isMe="false" />
        </li>

      </ol>
    </div>
    <div class="input-area">
      <div class="attach-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          class="bi bi-plus-circle-fill"
          viewBox="0 0 16 16"
        >
          <path
            d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"
          />
        </svg>
      </div>
      <textarea class="text-input"></textarea>
      <div class="send-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          class="bi bi-send"
          viewBox="0 0 16 16"
        >
          <path
            d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"
          />
        </svg>
      </div>
    </div>
  </div>
</template>
