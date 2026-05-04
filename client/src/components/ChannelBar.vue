<script setup>
import "../assets/channel-bar.css";
import { watch, ref, computed } from "vue";

const emit = defineEmits(["update-currentChannel", "update-chatChannels", "wake-agent", "open-agent-modal", "sleep-agent", "update-search-tab"]);

const selectChannel = (channelId) => {
  emit("update-currentChannel", channelId);
};

const selectSearchTab = (searchTab) => {
  emit("update-search-tab", searchTab);
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

      <p class="label">Your Agents</p>

      <template v-if="this.agents.length == 0">
        <div style="width: 100%; height: 150px; display: flex; align-items: center; justify-content: center;">
          <div style="text-align: center; width: 200px; color: var(--secondary)">
            You haven't created any agents yet.
          </div>
        </div>
      </template>
      <template v-for="agent in this.agents">
        <div class="channel-thumb mt-2" style="display: flex; flex-direction: row; justify-content: space-between; align-items: center;">
          <div style="display: flex; flex-direction: row;">
            <div :class="{'avatar': true, 'agent-llama': (agent.model == 'llama3.2'), 'agent-gemma': (agent.model == 'gemma3')}" v-if="[1, 3].includes(agent.status)">
                <i class="bi bi-stars"></i>
            </div>
            <div class="spinner-border custom-spinner" v-if="[0, 2].includes(agent.status)">
              <span class="visually-hidden">Loading...</span>
            </div>
            <div style="margin-left: 15px;">
              <p style="margin: 0;">{{ agent.name }} ({{ agent.model }})</p>
              <p style="margin: 0; font-size: 12px;" v-if="agent.status == 0">Initializing...</p>
              <p style="margin: 0; font-size: 12px; color: green;" v-if="agent.status == 1">Ready</p>
              <p style="margin: 0; font-size: 12px;" v-if="agent.status == 2">Typing...</p>
              <p style="margin: 0; font-size: 12px;" v-if="agent.status == 3">Sleeping</p>
            </div>
          </div>
          <div class="dropdown">
            <p role="button" data-bs-toggle="dropdown" aria-expanded="false" style="margin: 0;"><i class="bi bi-three-dots-vertical"></i></p>

            <ul class="dropdown-menu" style="width: 300px; background: #151626; border: 2px solid rgba(255, 255, 255, 0.12);">
              <li><a class="dropdown-item" v-if="agent.status == 3" @click="$emit('open-agent-modal', agent)">Edit agent settings</a></li>
              <li><a class="dropdown-item" v-if="agent.status == 3" @click="$emit('wake-agent', agent.id)">Wake agent</a></li>
              <li><a class="dropdown-item" style="color: #BB2D3C !important;" v-if="agent.status != 3" @click="$emit('sleep-agent', agent.id)">Send agent to sleep</a></li>
            </ul>
          </div>
        </div>
      </template>

    </div>

    <div v-if="currentServer == 'search'">
      <div :class="{'channel-thumb': true, 'active': (this.currentSearchTab == 0)}" @click="selectSearchTab(0)">
        <span style="font-weight: 700">Search</span>
      </div>

      <div :class="{'channel-thumb': true, 'active': (this.currentSearchTab == 1)}" @click="selectSearchTab(1)">
        <span style="font-weight: 700">Results</span>
      </div>
    </div>

    <div v-if="currentServer != 'home' && currentServer != 'search'">
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
    currentSearchTab: {
      type: Number,
      required: true,
    },
    agents: {
      type: Object,
      required: true,
    },
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
      if (newServer !== "home" && newServer !== "search") {
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
        this.$emit("update-chatChannels", response.data);
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
