<script setup>
import "../assets/chat-window.css";

import Message from "./Message.vue";

defineProps({
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
  },
});
</script>

<template>
  <div
    class="chat-window unselected"
    style="color: var(--secondary)"
    v-if="currentChannel == null"
  >
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
        <template v-for="(messageList, day) in messages" :key="day">
          <li class="message-list-item">
            <div class="date-label">{{ formatDay(day) }}</div>
          </li>
          <li
            class="message-list-item"
            v-for="message in messageList"
            :key="message.id"
          >
            <Message
              :message="message"
              :isMe="
                message.author.id === currentUser.id &&
                message.author.type != 'AGENT'
              "
            />
          </li>
        </template>
      </ol>
    </div>
    <div class="composer">
      <div class="selected-attachments" v-if="selectedFiles.length > 0">
        <div
          class="selected-attachment"
          v-for="(item, index) in selectedFiles"
          :key="item.id"
        >
          <img
            v-if="item.previewUrl"
            class="selected-attachment-preview"
            :src="item.previewUrl"
            alt=""
          />
          <div class="selected-attachment-icon" v-if="!item.previewUrl">
            <i class="bi bi-file-earmark"></i>
          </div>
          <div class="selected-attachment-details">
            <span class="selected-attachment-name">{{ item.file.name }}</span>
            <span class="selected-attachment-size">{{
              formatFileSize(item.file.size)
            }}</span>
          </div>
          <button
            class="remove-attachment"
            type="button"
            @click="removeSelectedFile(index)"
            aria-label="Remove attachment"
          >
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
      <p class="upload-error" v-if="uploadError">{{ uploadError }}</p>
      <div class="input-area">
        <textarea
          v-model="messageContent"
          class="text-input send-message"
          placeholder="Send a message..."
        ></textarea>
        <input
          ref="fileInput"
          class="file-input"
          type="file"
          multiple
          :accept="acceptedAttachmentTypes"
          @change="handleFileSelection"
        />
        <button
          class="action-button"
          type="button"
          @click="openFilePicker"
          aria-label="Attach files"
        >
          <i class="bi bi-paperclip" style="font-size: 25px"></i>
        </button>
        <button
          class="action-button"
          type="button"
          :disabled="sendingMessage"
          @click="postMessage(messageContent)"
          aria-label="Send message"
        >
          <i class="bi bi-send" style="font-size: 25px"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";

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
      messageContent: "",
      channel: null,
      selectedFiles: [],
      uploadError: null,
      sendingMessage: false,
      maxFiles: 5,
      maxFileSize: 10 * 1024 * 1024,
      allowedAttachmentTypes: new Set([
        "application/json",
        "application/msword",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/gif",
        "image/jpeg",
        "image/png",
        "image/webp",
        "text/csv",
        "text/markdown",
        "text/plain",
      ]),
      allowedAttachmentExtensions: new Set([
        "csv",
        "doc",
        "docx",
        "gif",
        "jpeg",
        "jpg",
        "json",
        "md",
        "pdf",
        "png",
        "txt",
        "webp",
      ]),
    };
  },
  computed: {
    acceptedAttachmentTypes() {
      return [
        ...Array.from(this.allowedAttachmentTypes),
        ...Array.from(this.allowedAttachmentExtensions).map(
          (extension) => `.${extension}`,
        ),
      ].join(",");
    },
  },
  methods: {
    async fetchMessages(channelId) {
      this.loading = true;

      if (this.channel) {
        this.pusher.unsubscribe(this.channel.name);
        this.channel = null;
      }
      let response = await this.$store.dispatch("message/fetchMessages", {
        payload: { channelId },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      this.messages = response.data;
      console.log("Fetched messages:", response);
      this.loading = false;

      this.channel = this.pusher.subscribe(
        `chat-channel-${this.currentChannel}`,
      );
      this.channel.bind("new-message", (message) => {
        const dateKey = moment(message.created_at).format("YYYY-MM-DD");
        if (!this.messages[dateKey]) {
          this.messages[dateKey] = [];
        }
        if (!this.messages[dateKey].some((m) => m.id === message.id)) {
          this.messages[dateKey].push(message);
        }

        setTimeout(() => {
          this.$refs.messagesContainer.scrollTop =
            this.$refs.messagesContainer.scrollHeight;
        }, 50);
      });

      setTimeout(() => {
        this.$refs.messagesContainer.scrollTop =
          this.$refs.messagesContainer.scrollHeight;
      }, 50);
    },
    async postMessage(content, replyToMessageId = null) {
      const trimmedContent = (content || "").trim();
      if (!trimmedContent && this.selectedFiles.length === 0) {
        return;
      }

      this.sendingMessage = true;
      this.uploadError = null;
      try {
        let response = await this.$store.dispatch("message/postMessage", {
          payload: {
            channelId: this.currentChannel,
            content: trimmedContent,
            replyToMessageId: replyToMessageId,
            files: this.selectedFiles.map((item) => item.file),
          },
          accessToken: await this.$auth0.getAccessTokenSilently(),
        });
        if (response.status === 201) {
          const message = response.data;
          const dateKey = moment(message.created_at).format("YYYY-MM-DD");
          if (!this.messages[dateKey]) {
            this.messages[dateKey] = [];
          }
          if (!this.messages[dateKey].some((m) => m.id === message.id)) {
            this.messages[dateKey].push(message);
          }
          this.messageContent = "";
          this.clearSelectedFiles();
        } else {
          console.error("Failed to post message:", response);
          this.uploadError = response?.data?.error || "Failed to send message.";
        }

        setTimeout(() => {
          this.$refs.messagesContainer.scrollTop =
            this.$refs.messagesContainer.scrollHeight;
        }, 50);
      } finally {
        this.sendingMessage = false;
      }
    },
    openFilePicker() {
      this.$refs.fileInput.click();
    },
    handleFileSelection(event) {
      this.uploadError = null;
      const files = Array.from(event.target.files || []);
      const nextFiles = [...this.selectedFiles];

      for (const file of files) {
        if (nextFiles.length >= this.maxFiles) {
          this.uploadError = `You can attach up to ${this.maxFiles} files per message.`;
          break;
        }

        if (file.size > this.maxFileSize) {
          this.uploadError = `${file.name} is larger than ${this.formatFileSize(this.maxFileSize)}.`;
          continue;
        }

        if (!this.isAllowedAttachment(file)) {
          this.uploadError = `${file.name} is not a supported file type.`;
          continue;
        }

        nextFiles.push({
          id: `${file.name}-${file.size}-${file.lastModified}-${Math.random()}`,
          file,
          previewUrl: file.type.startsWith("image/")
            ? URL.createObjectURL(file)
            : null,
        });
      }

      this.selectedFiles = nextFiles;
      event.target.value = "";
    },
    removeSelectedFile(index) {
      const [removed] = this.selectedFiles.splice(index, 1);
      if (removed?.previewUrl) {
        URL.revokeObjectURL(removed.previewUrl);
      }
    },
    clearSelectedFiles() {
      this.selectedFiles.forEach((item) => {
        if (item.previewUrl) {
          URL.revokeObjectURL(item.previewUrl);
        }
      });
      this.selectedFiles = [];
    },
    formatFileSize(bytes) {
      if (bytes < 1024) {
        return `${bytes} B`;
      }
      if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(1)} KB`;
      }
      return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    },
    isAllowedAttachment(file) {
      const extension = file.name.split(".").pop()?.toLowerCase();
      return (
        this.allowedAttachmentTypes.has(file.type) ||
        this.allowedAttachmentExtensions.has(extension)
      );
    },
    formatDay(dateString) {
      return moment(dateString, "YYYY-MM-DD").format("MMMM Do, YYYY");
    },
  },
  beforeUnmount() {
    this.clearSelectedFiles();
  },
};
</script>
