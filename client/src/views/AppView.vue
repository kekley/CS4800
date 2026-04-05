<script setup>
import ServerBar from "../components/ServerBar.vue";
import ChannelBar from "../components/ChannelBar.vue";
import ChatWindow from "../components/ChatWindow.vue";
import logo from "../assets/images/st-logo-light.svg";
import logoFlat from "../assets/images/st-logo-flat.svg";
</script>

<template>
  <!-- BEGIN Create/Join Server Modal -->
  <div class="modal fade" id="createJoinModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" style="max-width: 650px !important">
      <div class="modal-content" style="
          background: var(--bg-0);
          padding: 10px;
          color: white;
          font-family: &quot;Ubuntu&quot;;
          max-width: 650px !important;
        ">
        <div class="row mb-2">
          <div class="col-6" style="margin: 0; padding: 0">
            <div :class="{
              'slider-tab': true,
              active: this.createJoinModal.tab == 0,
            }" @click="this.createJoinModal.tab = 0">
              Create a Server
            </div>
          </div>
          <div class="col-6" style="margin: 0; padding: 0">
            <div :class="{
              'slider-tab': true,
              active: this.createJoinModal.tab == 1,
            }" @click="this.createJoinModal.tab = 1">
              Join a Server
            </div>
          </div>
        </div>

        <div v-if="this.createJoinModal.tab == 0" style="padding: 10px">
          <input class="text-input mb-2" v-model="this.createJoinModal.name" placeholder="Server Name"
            style="width: 100% !important; padding: 7px 10px" />
          <input class="text-input mb-2" v-model="this.createJoinModal.icon_url" placeholder="Icon URL"
            style="width: 100% !important; padding: 7px 10px" />
          <textarea class="text-input mb-2" v-model="this.createJoinModal.description" placeholder="Description"
            style="width: 100% !important; padding: 7px 10px" rows="3"></textarea>

          <div class="row mb-2">
            <div class="col-6">
              <div class="form-check">
                <input class="form-check-input" v-model="this.createJoinModal.public" type="checkbox" value=""
                  id="checkDefault" />
                <label class="form-check-label" for="checkDefault">
                  Make this server public?
                </label>
              </div>
            </div>
            <div class="col-6"></div>
          </div>

          <p style="color: red" v-if="this.createJoinModal.createError != null">
            {{ this.createJoinModal.createError }}
          </p>
          <button class="button mt-1" style="width: 100%" @click="createServer()">
            Create Server
          </button>
        </div>

        <div v-if="this.createJoinModal.tab == 1" style="padding: 10px">
          <p style="margin: 0" class="mb-2">
            Please enter your invite code in order to join the server
          </p>
          <input class="text-input mb-2" placeholder="Invite Code" style="width: 100% !important; padding: 7px 10px" />

          <p style="color: red" v-if="this.createJoinModal.joinError != null">
            {{ this.createJoinModal.joinError }}
          </p>
          <button class="button mt-1" style="width: 100%">Join Server</button>
        </div>
      </div>
    </div>
  </div>
  <!-- END Create/Join Server Modal -->

  <div class="loading" v-if="!this.ready || this.needsUsername">
    <img :src="logo" style="width: 200px" /> <br />

    <div class="spinner-border custom-spinner" role="status" v-if="!this.ready && !this.needsUsername">
      <span class="visually-hidden">Loading...</span>
    </div>

    <div v-if="this.needsUsername" style="text-align: center; width: 400px">
      <h3 style="margin: 0">Welcome to SmallTalk, {{ user.given_name }}!</h3>
      <p style="margin: 0; margin-top: 15px; font-size: 18px">
        We're excited you're here. We need a name to call you in order to get
        started.
      </p>
      <input v-model="desiredDisplayName" class="text-input" placeholder="Display Name"
        style="width: 100% !important; padding: 7px 10px; margin-top: 25px" />
      <input v-model="desiredUsername" class="text-input" placeholder="Username"
        style="width: 100% !important; padding: 7px 10px; margin-top: 10px" />
      <p style="margin: 0; color: red; margin-top: 15px" v-if="this.hasUsernameError">
        Sorry, that username is already taken.
      </p>
      <button class="button" style="margin-top: 25px; width: 300px" @click="submitUsername()">
        Let's Go!
      </button>
    </div>
  </div>

  <div class="main" v-if="this.ready && !this.needsUsername">
    <div class="head-nav">
      <img :src="logo" style="width: 125px" />
      <input class="text-input" placeholder="Search your messages..."
        style="width: 400px !important; padding: 7px 10px" />
    </div>
    <div class="top-bar">
      {{this.userServers.find(s => s.id == this.currentServer)?.name || "Home"}}
    </div>
    <div class="app-window">
      <div style="display: flex; flex-direction: column">
        <div style="
            display: flex;
            flex-direction: row;
            flex: 1;
            overflow-y: scroll;
          ">
          <div class="server-sidebar">
            <ServerBar :servers="this.userServers" :currentServer="this.currentServer"
              @update-currentServer="this.currentServer = $event" />
          </div>
          <div class="left-sidebar">
            <ChannelBar :currentServer="this.currentServer" :currentChannel="this.currentChannel"
              @update-currentChannel="this.currentChannel = $event" />
          </div>
        </div>

        <div class="connection-status">
          <p class="text-success" style="
              margin: 0;
              font-size: 18px;
              font-weight: 700;
              margin-bottom: 2px;
            " v-if="false">
            Connected to Web RTC
          </p>
          <div class="overall-status">
            <div style="display: flex; align-items: center">
              <div :class="{
                'spinner-grow': true,
                'text-warning': this.ws_info.connectionState == null,
                'text-success': this.ws_info.connectionState == 2,
              }" role="status" style="width: 12px; height: 12px; margin-right: 7px"></div>
              <template v-if="this.ws_info.connectionState == null">Connecting to real-time services...</template>
              <template v-if="this.ws_info.connectionState == 2">Connceted to SmallTalk real-time services</template>
              <template v-if="this.ws_info.connectionState == 3">Unable to connect to SmallTalk real-time
                services</template>
            </div>
            <p style="font-size: 12px; color: #d3d3d3; margin: 0">
              {{
                this.ws_info.latency == null ? "" : `${this.ws_info.latency}ms`
              }}
            </p>
          </div>
        </div>

        <div class="status-center">
          <div class="dropdown">
            <div class="account-center" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">
              <img :src="user.picture" class="profile" />
              <div>
                <p style="margin: 0; font-weight: 700">
                  {{ userInfo.displayName }}
                </p>
                <p style="margin: 0; font-weight: 400; font-size: 12px">
                  @{{ userInfo.username }}
                </p>
              </div>
            </div>
            <div class="dropdown-menu p-3" style="
                width: 300px;
                background: #151626;
                border: 2px solid rgba(255, 255, 255, 0.12);
              ">
              <p style="
                  font-size: 20px;
                  color: #f2f2f2;
                  margin: 0;
                  font-weight: 700;
                ">
                {{ user.given_name }} {{ user.family_name }}
              </p>
              <p style="margin: 0; color: #f2f2f2; font-size: 15px" class="mb-3">
                Signed in as <strong>{{ user.email }}</strong>
              </p>
              <button @click="logout()" type="button" class="btn btn-danger w-100">
                Logout
              </button>
            </div>
          </div>

          <div style="display: flex; flex-direction: row">
            <p style="
                margin: 0;
                font-size: 20px;
                margin-left: 20px;
                cursor: pointer;
              ">
              <i class="bi bi-mic-fill"></i>
            </p>
            <p style="
                margin: 0;
                font-size: 20px;
                margin-left: 20px;
                cursor: pointer;
              ">
              <i class="bi bi-volume-up-fill"></i>
            </p>
          </div>
        </div>
      </div>
      <div class="main-content" v-if="this.currentServer != 'home'">
        <ChatWindow :currentChannel="this.currentChannel" />
      </div>
      <div class="right-sidebar" v-if="this.currentServer != 'home'">
        <!-- <MemberBar :server="this.currentServer" /> -->
        <p style="margin: 0; font-weight: 700">Members</p>
      </div>
      <div class="home-content" v-if="this.currentServer == 'home'">
        <div style="text-align: center">
          <img :src="logoFlat" style="width: 250px" /> <br />
          <p style="margin: 0; font-size: 32px; font-weight: 0; margin-top: 25px">
            <strong>Welcome, @{{ userInfo.username }}!</strong>
          </p>
          <p style="margin: 0; font-size: 28px; font-weight: 0">
            Select a server to get started ({{ this.currentServer }})
          </p>

          <div style="
              display: flex;
              flex-direction: row;
              align-items: center;
              justify-content: center;
              margin-top: 25px;
            ">
            <div style="
                width: 150px;
                display: flex;
                justify-content: center;
                align-items: center;
              ">
              <div>
                <p style="margin: 0; color: #674ea7; font-size: 45px">0</p>
                <p>message(s) sent</p>
              </div>
            </div>
            <div style="
                width: 150px;
                height: 100px;
                display: flex;
                justify-content: center;
                align-items: center;
              ">
              <div>
                <p style="margin: 0; color: #674ea7; font-size: 45px">0</p>
                <p>friend(s)</p>
              </div>
            </div>
            <div style="
                width: 150px;
                height: 100px;
                display: flex;
                justify-content: center;
                align-items: center;
              ">
              <div>
                <p style="margin: 0; color: #674ea7; font-size: 45px">0</p>
                <p>server(s) owned</p>
              </div>
            </div>
          </div>

          <div style="margin-top: 25px">
            <button class="button" style="width: 300px; background: #444552" data-bs-toggle="modal"
              data-bs-target="#createJoinModal" @click="this.createJoinModal.tab = 0">
              Create a Server
            </button>
            <button class="button" style="width: 300px; background: #444552; margin-left: 15px" data-bs-toggle="modal"
              data-bs-target="#createJoinModal" @click="this.createJoinModal.tab = 1">
              Join a Server
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuth0 } from "@auth0/auth0-vue";
import { create, has } from "lodash-es";
import server from "@/store/modules/server";

export default {
  data() {
    const { logout, user, isAuthenticated } = useAuth0();
    return {
      ready: false,
      logout: () => {
        logout({
          logoutParams: {
            returnTo: window.location.origin,
          },
        });
      },
      ws_info: {
        connectionState: null,
        latency: null,
      },
      createJoinModal: {
        tab: 0,
        name: null,
        description: null,
        icon_url: null,
        public: false,
        createError: null,
        joinError: null,
      },

      userServers: [],
      serverChannels: null,
      currentServer: "home",
      currentChannel: null,
      currentMembers: null,
      user,
      userInfo: null,
      needsUsername: false,
      hasUsernameError: false,
      isAuthenticated,
    };
  },
  async mounted() {
    await this.loadUserInfo();
    await this.loadUserServers();
    this.ready = true;
    this.initPusherConnection();
  },
  methods: {
    async loadUserInfo() {
      this.userInfo = await this.$store.dispatch("user/getUserInfo", {
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      if (this.userInfo.username == null) {
        this.needsUsername = true;
      }
    },
    async loadUserServers() {
      this.userServers = await this.$store.dispatch("server/listUserServers", {
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
    },

    async submitUsername() {
      let response = await this.$store.dispatch("user/updateUserInfo", {
        updates: {
          displayName: this.desiredDisplayName,
          username: this.desiredUsername,
        },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      if (response == 204) {
        this.needsUsername = false;
        this.userInfo.displayName = this.desiredDisplayName;
        this.userInfo.username = this.desiredUsername;
      } else {
        this.hasUsernameError = true;
      }
    },
    async createServer() {
      let response = await this.$store.dispatch("server/createServer", {
        payload: {
          name: this.createJoinModal.name,
          description: this.createJoinModal.description,
          icon_url: this.createJoinModal.icon_url,
          public: this.createJoinModal.public,
        },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      if (response.status && response.status != 201) {
        this.createJoinModal.createError = response.data.message;
      } else {
        this.userServers.push(response.data);
        this.currentServer = response.data.id;
        this.createJoinModal.name = null;
        this.createJoinModal.description = null;
        this.createJoinModal.icon_url = null;
        this.createJoinModal.public = false;
        this.createJoinModal.createError = null;
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("createJoinModal"),
        );
        modal.hide();
      }

    },

    initPusherConnection() {
      Pusher.logToConsole = true;

      var pusher = new Pusher("8e27f35d62403a6df5b7", {
        cluster: "us3",
      });

      pusher.connection.bind("connected", () => {
        this.ws_info.connectionState = 2;
        const pingTime = Date.now();
        const testChannel = pusher.subscribe("public-latency-test");
        testChannel.bind("pusher:subscription_succeeded", () => {
          const pongTime = Date.now();
          this.ws_info.latency = pongTime - pingTime;
          console.log("TEST");
        });
      });
      pusher.connection.bind("unavailable", () => {
        this.ws_info.connectionState = 3;
      });
    },
    openCreateJoinModal() {
      Object.assign(this.createJoinModal, {
        name: null,
        description: null,
        icon_url: null,
        public: false,
        createError: null,
      });
    },

  },
};
</script>
