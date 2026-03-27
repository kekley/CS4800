<script setup>
import "../assets/chat-window.css";

import { ref, computed } from "vue";
import Message from "./Message.vue";

import axios from "axios";
import { useAuth0 } from '@auth0/auth0-vue';
import { useApi } from '../api.js';

const auth0Client = useAuth0();


async function me() {

    const api = useApi(auth0Client.getAccessTokenSilently);

    const res = await api.get(`/api/me`, 
    api);
    console.log(res);
    
    return res.data;
}


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
  user: "Sam Altman",
  text: "hello",
  time: "1:57PM",
};

</script>

<template>
  <div class="chat-window">
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
        <i class="bi bi-paperclip" style="font-size: 25px;"></i>
      </div>
      <div class="action-button" @click="me()">
        <i class="bi bi-send" style="font-size: 25px;"></i>
      </div>
    </div>
  </div>
</template>
