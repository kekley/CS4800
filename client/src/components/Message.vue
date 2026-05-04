<template>
  <div :class="['chat-message', { me: isMe }]">
    <div class="container">
      <img
        class="avatar"
        :src="message.author.avatar_url"
        v-if="message.author.type == 'USER'"
      />
      <div
        :class="{
          avatar: true,
          'agent-llama': message.author.model == 'llama3.2',
          'agent-gemma': message.author.model == 'gemma3',
        }"
        v-if="message.author.type == 'AGENT'"
      >
        <i class="bi bi-stars"></i>
      </div>
      <div class="vertical">
        <div class="header">
          <span class="username" v-if="message.author.type == 'USER'">{{
            message.author.username
          }}</span>
          <span class="username" v-if="message.author.type == 'AGENT'"
            >{{ message.author.name }} ({{ message.author.model }})</span
          >
          <span class="timestamp">{{ formatTime(message.created_at) }}</span>
        </div>
        <div class="contents">
          <span v-if="message.content" class="message-text">{{
            message.content
          }}</span>
          <template
            v-for="attachment in message.attachments || []"
            :key="attachment.id"
          >
            <div v-if="isImageAttachment(attachment)" class="attachment-image">
              <img
                v-if="attachmentObjectUrls[attachment.id]"
                :src="attachmentObjectUrls[attachment.id]"
                :alt="attachment.file_name"
              />
              <button
                v-else
                class="attachment-file"
                type="button"
                @click="downloadAttachment(attachment)"
              >
                <i class="bi bi-image"></i>
                <span>{{ attachment.file_name }}</span>
              </button>
            </div>
            <button
              v-else
              class="attachment-file"
              type="button"
              @click="downloadAttachment(attachment)"
            >
              <i class="bi bi-file-earmark-arrow-down"></i>
              <span>{{ attachment.file_name }}</span>
              <small>{{ formatFileSize(attachment.size) }}</small>
            </button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "../assets/chat-message.css";

import moment from "moment";
import Api from "@/services/api";

export default {
  name: "Message",
  props: {
    message: {
      type: Object,
      required: true,
    },
    isMe: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      attachmentObjectUrls: {},
    };
  },
  watch: {
    message: {
      immediate: true,
      deep: true,
      handler() {
        this.loadImageAttachments();
      },
    },
  },
  beforeUnmount() {
    this.revokeAttachmentObjectUrls();
  },
  methods: {
    formatTime(dateString) {
      return moment.utc(dateString).local().format("h:mm A");
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
    isImageAttachment(attachment) {
      return attachment.type && attachment.type.startsWith("image/");
    },
    async attachmentBlob(attachment, usePreview = false) {
      const accessToken = await this.$auth0.getAccessTokenSilently();
      const response = await Api().get(
        usePreview ? attachment.preview_url : attachment.url,
        {
          responseType: "blob",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        },
      );
      return response.data;
    },
    async loadImageAttachments() {
      const imageAttachments = (this.message.attachments || []).filter(
        (attachment) =>
          this.isImageAttachment(attachment) &&
          !this.attachmentObjectUrls[attachment.id],
      );

      for (const attachment of imageAttachments) {
        try {
          const blob = await this.attachmentBlob(attachment, true);
          this.attachmentObjectUrls = {
            ...this.attachmentObjectUrls,
            [attachment.id]: URL.createObjectURL(blob),
          };
        } catch (error) {
          console.error("Failed to load attachment preview:", error);
        }
      }
    },
    async downloadAttachment(attachment) {
      try {
        const blob = await this.attachmentBlob(attachment);
        const objectUrl = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = objectUrl;
        link.download = attachment.file_name;
        document.body.appendChild(link);
        link.click();
        link.remove();
        setTimeout(() => URL.revokeObjectURL(objectUrl), 0);
      } catch (error) {
        console.error("Failed to download attachment:", error);
      }
    },
    revokeAttachmentObjectUrls() {
      Object.values(this.attachmentObjectUrls).forEach((objectUrl) => {
        URL.revokeObjectURL(objectUrl);
      });
      this.attachmentObjectUrls = {};
    },
  },
};
</script>
