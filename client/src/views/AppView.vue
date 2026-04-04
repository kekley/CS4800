<script setup>
import ServerBar from "../components/ServerBar.vue";
import ChannelBar from "../components/ChannelBar.vue";
import ChatWindow from "../components/ChatWindow.vue";

import logo from '../assets/images/st-logo-light.svg';
import logoFlat from '../assets/images/st-logo-flat.svg';
</script>

<template>
  <!-- BEGIN Create/Join Server Modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content" style="background: var(--secondary); padding: 10px; color: white;">
        test
      </div>
    </div>
  </div>
  <!-- END Create/Join Server Modal -->

  <div class="loading" v-if="!this.ready || this.needsUsername">
    <img :src="logo" style="width: 200px;"> <br>

    <div class="spinner-border custom-spinner" role="status" v-if="!this.ready && !this.needsUsername">
      <span class="visually-hidden">Loading...</span>
    </div>

    <div v-if="this.needsUsername" style="text-align: center; width: 400px;">
      <h3 style="margin: 0;">Welcome to SmallTalk, {{ user.given_name }}!</h3>
      <p style="margin: 0; margin-top: 15px; font-size: 18px; ">We're excited you're here. We need a name to call you in order to get started.</p>

      <input v-model="desiredDisplayName" class="text-input" placeholder="Display Name" style="width: 100% !important; padding: 7px 10px; margin-top: 25px;" /> 
      <input v-model="desiredUsername" class="text-input" placeholder="Username" style="width: 100% !important; padding: 7px 10px; margin-top: 10px;" /> 
      <p style="margin: 0; color: red; margin-top: 15px;" v-if="this.hasUsernameError">Sorry, that username is already taken.</p>
      
      <button class="button" style="margin-top: 25px; width: 300px;" @click="submitUsername()">Let's Go!</button>
    </div>
  </div>

  <div class="main" v-if="this.ready && !this.needsUsername">
    <div class="head-nav">
      <img :src="logo" style="width: 125px;">
      <input class="text-input" placeholder="Search your messages..." style="width: 400px !important; padding: 7px 10px;" /> 
    </div>
    <div class="top-bar">
      <template v-if="this.currentServer != 'home'">{{ this.currentServer }}</template>
    </div>
    <div class="app-window">
      <div style="display: flex; flex-direction: column;">
        
        <div style="display: flex; flex-direction: row; flex: 1; overflow-y: scroll;">
          <div class="server-sidebar">
            <ServerBar 
              :servers="this.userServers" 
              :currentServer="this.currentServer"
              @update-currentServer="this.currentServer = $event; this.currentChannel = null" />
          </div>
          <div class="left-sidebar">
            <ChannelBar 
              :currentServer="this.currentServer"
              :currentChannel="this.currentChannel"
              @update-currentChannel="this.currentChannel = $event"/>
          </div>
        </div>

        <div class="connection-status">
          <p class="text-success" style="margin: 0; font-size: 18px; font-weight: 700; margin-bottom: 2px;" v-if="false">Connected to Web RTC</p>
          <div class="overall-status">
            <div style="display: flex; align-items: center;">
              <div :class="{'spinner-grow': true, 'text-warning': (this.ws_info.connectionState == null), 'text-success': (this.ws_info.connectionState == 2)}" role="status" style="width: 12px; height: 12px; margin-right: 7px;"></div> 
              <template v-if="this.ws_info.connectionState == null">Connecting to real-time services...</template>
              <template v-if="this.ws_info.connectionState == 2">Connceted to SmallTalk real-time services</template>
              <template v-if="this.ws_info.connectionState == 3">Unable to connect to SmallTalk real-time services</template>


            </div>
          <p style="font-size: 12px; color: #d3d3d3; margin: 0;">{{ (this.ws_info.latency == null) ? 'Pinging...' : `${this.ws_info.latency}ms` }}</p>
          </div>
        </div>

        <div class="status-center">

          <div class="dropdown">
            <div class="account-center" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">
              <img :src="user.picture" class="profile">
              <div>
                <p style="margin: 0; font-weight: 700;">{{ userInfo.displayName }}</p>
                <p style="margin: 0; font-weight: 400; font-size: 12px;">@{{ userInfo.username }}</p>
              </div>
            </div>
            <div class="dropdown-menu p-3" style="width: 300px; background: #151626; border: 2px solid rgba(255, 255, 255, 0.12);">
              <p style="font-size: 20px; color: #f2f2f2; margin: 0; font-weight: 700;">{{ user.given_name }} {{ user.family_name }}</p>
              <p style="margin: 0; color: #f2f2f2; font-size: 15px;" class="mb-3">Signed in as <strong>{{ user.email }}</strong></p>
              <button @click="logout()" type="button" class="btn btn-danger w-100">Logout</button>
            </div>
          </div>

          <div style="display: flex; flex-direction: row;">
            <p style="margin: 0; font-size: 20px; margin-left: 20px; cursor: pointer;"><i class="bi bi-mic-fill"></i></p>
            <p style="margin: 0; font-size: 20px; margin-left: 20px; cursor: pointer;"><i class="bi bi-volume-up-fill"></i></p>
          </div>

        </div>

      </div>
      <div class="main-content" v-if="this.currentServer != 'home'">
        <ChatWindow :currentChannel="this.currentChannel" />
      </div>
      <div class="right-sidebar" v-if="this.currentServer != 'home'">
        <!-- <MemberBar :server="this.currentServer" /> -->
        <p style="margin: 0; font-weight: 700;">Members</p>
      </div>
      <div class="home-content" v-if="this.currentServer == 'home'">
        <div style="text-align: center;">
          <img :src="logoFlat" style="width: 250px;"> <br>
          <p style="margin: 0; font-size: 32px; font-weight: 0; margin-top: 25px;"><strong>Welcome, @{{ userInfo.username }}!</strong></p>
          <p style="margin: 0; font-size: 28px; font-weight: 0;">Select a server to get started</p>
          
          <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; margin-top: 25px;">
            <div style="width: 150px; display: flex; justify-content: center; align-items: center;">
              <div>
                <p style="margin: 0; color: #674ea7; font-size: 45px;">0</p>
                <p>message(s) sent</p>
              </div>
            </div>
            <div style="width: 150px; height: 100px; display: flex; justify-content: center; align-items: center;">
              <div>
                <p style="margin: 0; color: #674ea7; font-size: 45px;">0</p>
                <p>friend(s)</p>
              </div>
            </div>
            <div style="width: 150px; height: 100px; display: flex; justify-content: center; align-items: center;">
              <div>
                <p style="margin: 0; color: #674ea7; font-size: 45px;">0</p>
                <p>server(s) owned</p>
              </div>
            </div>
          </div>

          <div style="margin-top: 25px;">
            <button class="button" style="width: 300px; background: #444552;">Create a Server</button>
            <button class="button" style="width: 300px; background: #444552; margin-left: 15px;">Join a Server</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuth0 } from '@auth0/auth0-vue';

export default {
    data() {
        const { logout, user, isAuthenticated } = useAuth0();
        return {
            ready: false,
            logout: () => {
                logout({
                    logoutParams: {
                        returnTo: window.location.origin
                    }
                });
            },
            ws_info: {
              connectionState: null,
              latency: null,
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
            isAuthenticated
        }
    },
    async mounted() {
      await this.loadUserInfo();
      await this.loadUserServers();
      this.ready = true;
      this.initPusherConnection();
    },
    methods: {
      async loadUserInfo() {
        this.userInfo = await this.$store.dispatch('user/getUserInfo', {
          accessToken: await this.$auth0.getAccessTokenSilently()
        });
        if (this.userInfo.username == null) {
          this.needsUsername = true;
        }
      },
      async loadUserServers() {
        this.userServers = await this.$store.dispatch('server/listUserServers', {
          accessToken: await this.$auth0.getAccessTokenSilently()
        });
        this.userServers = ["A", "B", "C"];
      },
      async submitUsername() {
        let response = await this.$store.dispatch('user/updateUserInfo', {
          updates: {
            displayName: this.desiredDisplayName,
            username: this.desiredUsername
          },
          accessToken: await this.$auth0.getAccessTokenSilently()
        });
        if (response == 204) {
          this.needsUsername = false;
          this.userInfo.displayName = this.desiredDisplayName;
          this.userInfo.username = this.desiredUsername;
        } else {
          this.hasUsernameError = true;
        }
      },
      initPusherConnection() {
        Pusher.logToConsole = true;

        var pusher = new Pusher('8e27f35d62403a6df5b7', {
          cluster: 'us3'
        });

        pusher.connection.bind("connected", () => {
            this.ws_info.connectionState = 2;
            const pingTime = Date.now();
            const testChannel = pusher.subscribe('public-latency-test');         
            testChannel.bind('pusher:subscription_succeeded', () => {
                const pongTime = Date.now();
                this.ws_info.latency = pongTime - pingTime;
                console.log("TEST");
            });
        });
        pusher.connection.bind("unavailable", () => {
            this.ws_info.connectionState = 3;
        });
      },
    }
}
</script>