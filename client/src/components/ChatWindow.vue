<script setup>
import "../assets/chat-window.css";

import { ref, computed } from "vue";
import Message from "./Message.vue";



const props = defineProps({
  currentChannel: {
    type: String,
    required: true,
  },
  currentUser: {
    type: Object,
    required: true,
  },
});

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
        <template v-for="message in messages" :key="message.id">
          <Message :message="message" :isMe="message.author.id === currentUser.id" />
        </template>

      </ol>
    </div>
    <div class="input-area">
      <textarea v-model="messageContent" class="text-input send-message" placeholder="Send a message..."></textarea>
      <div class="action-button">
        <i class="bi bi-paperclip" style="font-size: 25px"></i>
      </div>
      <div class="action-button" @click="postMessage(messageContent)">
        <i class="bi bi-send" style="font-size: 25px"></i>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "ChatWindow",
  watch: {
    currentChannel(newVal) {
      this.fetchMessages(newVal);
    },
  },
  data() {
    return {
      messages: [],
      messageContent: "",
    };
  },
  methods: {
    async fetchMessages(channelId) {
      let response = await this.$store.dispatch("message/fetchMessages", {
        payload: { channelId },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      this.messages = response.data;
      console.log("Fetched messages:", response);
    },
    async postMessage(content, replyToMessageId = null) {
      let response = await this.$store.dispatch("message/postMessage", {
        payload: { channelId: this.currentChannel, content: content, replyToMessageId },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      if (response.status === 201) {
        this.fetchMessages(this.currentChannel);
      } else {
        console.error("Failed to post message:", response);
      }
    },
  },
};
</script>