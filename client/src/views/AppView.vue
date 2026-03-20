<script setup>
import ServerBar from "../components/ServerBar.vue";
import ChannelBar from "../components/ChannelBar.vue";
import ChatWindow from "../components/ChatWindow.vue";

import logo from '../assets/images/st-logo-light.svg'

import { ref, computed } from "vue";

</script>

<template>
  <div class="loading" v-if="!this.ready">
    <img :src="logo" style="width: 200px;"> <br>
    <div class="spinner-border custom-spinner" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <div class="main" v-if="this.ready">
    <div class="head-nav">
      <img :src="logo" style="width: 125px;">
      <input class="text-input" placeholder="Search your messages..." style="width: 400px !important; padding: 7px 10px;" /> 
    </div>
    <div class="top-bar">
      Example Server A
    </div>
    <div class="app-window">
      <div style="display: flex; flex-direction: column;">
        
        <div style="display: flex; flex-direction: row; flex: 1; overflow-y: scroll;">
          <div class="server-sidebar">
            <ServerBar :user="this.user" />
          </div>
          <div class="left-sidebar">
            <ChannelBar />
          </div>
        </div>

        <div class="connection-status">
          <p class="text-success" style="margin: 0; font-size: 18px; font-weight: 700; margin-bottom: 2px;" v-if="false">Connected to Web RTC</p>
          <div class="overall-status">
            <div style="display: flex; align-items: center;">
              <div class="spinner-grow text-success" role="status" style="width: 12px; height: 12px; margin-right: 7px;"></div> 
              Connceted to SmallTalk real-time services
            </div>
          <p style="font-size: 12px; color: #d3d3d3; margin: 0;">5ms</p>
          </div>
        </div>

        <div class="status-center">

          <div class="dropdown">
            <div class="account-center" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">
              <img :src="user.picture" class="profile">
              <div>
                <p style="margin: 0; font-weight: 700;">{{ user.given_name }} {{ user.family_name }}</p>
                <p style="margin: 0; font-weight: 400; font-size: 12px;">@tdnakfoor</p>
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
      <div class="main-content">
        <ChatWindow />
      </div>
      <div class="right-sidebar">
        <p style="margin: 0; font-weight: 700;">Members</p>
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
            loading: true,
            ready: true,
            logout: () => {
                logout({
                    logoutParams: {
                        returnTo: window.location.origin
                    }
                });
            },
            user,
            userInfo: null,
            isAuthenticated
        }
    },
    async mounted() {

    }
}
</script>