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
      <textarea class="text-input"></textarea>
      <div class="send-button">

      </div>
    </div>
  </div>
</template>
