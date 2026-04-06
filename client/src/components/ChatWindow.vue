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
  pusher: {
    type: Object,
    required: true,
  }
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

  <div class="chat-window unselected" v-if="currentChannel != null && loading">
    <div class="spinner-border custom-spinner" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <div class="chat-window" v-if="currentChannel != null && !loading">
    <div class="messages" ref="messagesContainer">
      <ol class="message-list">
        <template v-for="(messageList, day) in messages">
          <li class="message-list-item">
            <div class="date-label">{{ formatDay(day) }}</div>
          </li>
          <li class="message-list-item" v-for="message in messageList">
            <Message :message="message" :isMe="message.author.id === currentUser.id" />
          </li>
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
import moment from 'moment';

export default {
  name: "ChatWindow",
  watch: {
    currentChannel(newVal) {
      this.fetchMessages(newVal);
    },
  },
  data() {
    return {
      loading: false,
      messages: {},
      messageContent: null,
      channel: null
    };
  },
  methods: {
    async fetchMessages(channelId) {
      this.loading = true;
      let response = await this.$store.dispatch("message/fetchMessages", {
        payload: { channelId },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      this.messages = response.data;
      console.log("Fetched messages:", response);
      this.loading = false;

      this.channel = this.pusher.subscribe(`chat-channel-${this.currentChannel}`);
      this.channel.bind('new-message', (message) => {
        const dateKey = moment(message.created_at).format('YYYY-MM-DD');
        if (!this.messages[dateKey]) {
          this.messages[dateKey] = [];
        }
        if (!this.messages[dateKey].some(m => m.id === message.id)) {
          this.messages[dateKey].push(message);
        }

        setTimeout(() => {
          this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
        }, 50);
      })

      setTimeout(() => {
        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
      }, 50);
    },
    async postMessage(content, replyToMessageId = null) {
      if (this.messageContent != null) {
        let response = await this.$store.dispatch("message/postMessage", {
          payload: { channelId: this.currentChannel, content: content, replyToMessageId },
          accessToken: await this.$auth0.getAccessTokenSilently(),
        });
        if (response.status === 201) {
          const message = response.data;
          const dateKey = moment(message.created_at).format('YYYY-MM-DD');
          if (!this.messages[dateKey]) {
            this.messages[dateKey] = [];
          }
          if (!this.messages[dateKey].some(m => m.id === message.id)) {
            this.messages[dateKey].push(message);
          }
          this.messageContent = null;
        } else {
          console.error("Failed to post message:", response);
        }

        setTimeout(() => {
          this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
        }, 50);
      }
    },
    formatDay(dateString) {
      return moment(dateString, 'YYYY-MM-DD').format('MMMM Do, YYYY');
    },
  },
};
</script>