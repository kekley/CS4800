<script setup>
import "../assets/channel-bar.css";
import { watch, ref, computed } from "vue";

const emit = defineEmits(["update-currentChannel"]);

const selectChannel = (channelId) => {
  emit("update-currentChannel", channelId);
};
</script>

<template>
  <!-- BEGIN Create Channel Modal -->
  <div class="modal fade" id="createChannelModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" style="max-width: 650px !important">
      <div class="modal-content" style="
          background: var(--bg-0);
          padding: 10px;
          color: white;
          font-family: 'Ubuntu';
          max-width: 650px !important;
        ">
        <div class="row mb-2">
          <div class="slider-tab active">Create a Channel</div>
        </div>

        <div style="padding: 10px">
          <input class="text-input mb-2" v-model="this.createChannelModal.name" placeholder="Channel Name"
            style="width: 100% !important; padding: 7px 10px" />
          <p style="color: red" v-if="this.createChannelModal.createError != null">
            {{ this.createChannelModal.createError }}
          </p>
          <button class="button mt-1" style="width: 100%" @click="createChannel(this.currentServer.id)">
            Create Channel
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- END Create Channel Modal -->

  <div class="channel-bar working" v-if="loading">
    <div class="spinner-border custom-spinner" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <div class="channel-bar" v-if="!loading">
    <div v-if="currentServer == 'home'">
      <p class="label">Your Friends</p>
    </div>

    <div v-if="currentServer != 'home'">
      <div style="
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 10px;
        ">
        <p class="label">Chat Channels</p>
        <button class="button" data-bs-toggle="modal" data-bs-target="#createChannelModal" style="
            padding: 5px 10px;
            background-color: rgb(68, 69, 82);
            font-size: 12px;
          " @click="openCreateChannelModal" v-if="currentServer.role < 2">
          <i class="bi bi-plus"></i>
        </button>
      </div>

      <template v-if="chatChannels.length == 0">
        <div style="width: 100%; height: 150px; display: flex; align-items: center; justify-content: center;">
          <div style="text-align: center; width: 200px; color: var(--secondary)">
            There are no chat channels in this server
          </div>
        </div>
      </template>
      <template v-for="channel in chatChannels">
        <div :class="{
          'channel-thumb': true,
          active: currentChannel == channel.id,
        }" @click="selectChannel(channel.id)">
          <span style="font-weight: 700"><i class="bi bi-hash"></i> {{ channel.name }}</span>
          <br />
          <div class="presence-indicator" v-if="channel.id == 10">
            <div class="spinner-grow text-success" role="status"></div>
            <p>5 members here</p>
          </div>
        </div>
      </template>

      <p class="label">Voice Channels</p>

      <template v-if="voiceChannels.length == 0">
        <div style="width: 100%; height: 150px; display: flex; align-items: center; justify-content: center;">
          <div style="text-align: center; width: 200px; color: var(--secondary)">
            There are no voice channels in this server
          </div>
        </div>
      </template>

    </div>
  </div>
</template>

<script>
export default {
  name: "ChannelBar",
  async mounted() { },
  data() {
    return {
      chatChannels: [],
      voiceChannels: [],
      createChannelModal: {
        name: null,
        createError: null,
      },
      loading: false,
    };
  },
  props: {
    currentServer: {
      type: Object,
      required: true,
    },
    currentChannel: {
      type: String,
      required: true,
    },
  },
  watch: {
    currentServer(newServer) {
      if (newServer !== "home") {
        this.fetchChannels(newServer.id);
      }
    },
  },
  methods: {
    async createChannel(serverId) {
      let response = await this.$store.dispatch("channel/createChannel", {
        payload: {
          name: this.createChannelModal.name,
          serverId: serverId,
        },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });

      if (response.status && response.status != 201) {
        this.createChannelModal.createError = response.data.message;
      } else {
        this.chatChannels.push(response.data);
        this.$emit("update-currentChannel", response.data.id);
        this.createChannelModal.name = null;
        this.createChannelModal.createError = null;
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("createChannelModal"),
        );
        modal.hide();
      }
    },
    async fetchChannels(serverId) {
      this.loading = true;
      let response = await this.$store.dispatch("channel/fetchChannels", {
        payload: {
          serverId: serverId,
        },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      if (response.status == 200) {
        this.chatChannels = response.data;
      } else {
        console.error("Error fetching channels:", response);
      }
      this.loading = false;
    },
  },
  openCreateChannelModal() {
    const modal = new bootstrap.Modal(
      document.getElementById("createChannelModal"),
    );
    modal._element.addEventListener("hidden.bs.modal", () => {
      Object.assign(this.createChannelModal, {
        name: null,
        createError: null,
      });
    });

    modal.show();
  },
};
</script>
