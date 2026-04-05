<script setup>
import ServerBar from "../components/ServerBar.vue";
import ChannelBar from "../components/ChannelBar.vue";
import ChatWindow from "../components/ChatWindow.vue";
import Message from "../components/Message.vue";
import logo from "../assets/images/st-logo-light.svg";
import logoFlat from "../assets/images/st-logo-flat.svg";
</script>

<template>
  <!-- BEGIN Create/Join Server Modal -->
  <div class="modal fade" id="createJoinModal" tabindex="-1" aria-hidden="true">
    <div
      class="modal-dialog modal-dialog-centered"
      style="max-width: 650px !important"
    >
      <div
        class="modal-content"
        style="
          background: var(--bg-0);
          padding: 10px;
          color: white;
          font-family: &quot;Ubuntu&quot;;
          max-width: 650px !important;
        "
      >
        <div class="row mb-2">
          <div class="col-6" style="margin: 0; padding: 0">
            <div
              :class="{
                'slider-tab': true,
                active: this.createJoinModal.tab == 0,
              }"
              @click="this.createJoinModal.tab = 0"
            >
              Create a Server
            </div>
          </div>
          <div class="col-6" style="margin: 0; padding: 0">
            <div
              :class="{
                'slider-tab': true,
                active: this.createJoinModal.tab == 1,
              }"
              @click="this.createJoinModal.tab = 1"
            >
              Join a Server
            </div>
          </div>
        </div>

        <div v-if="this.createJoinModal.tab == 0" style="padding: 10px">
          <input
            class="text-input mb-2"
            v-model="this.createJoinModal.name"
            placeholder="Server Name"
            style="width: 100% !important; padding: 7px 10px"
          />
          <input
            class="text-input mb-2"
            v-model="this.createJoinModal.icon_url"
            placeholder="Icon URL"
            style="width: 100% !important; padding: 7px 10px"
          />
          <textarea
            class="text-input mb-2"
            v-model="this.createJoinModal.description"
            placeholder="Description"
            style="width: 100% !important; padding: 7px 10px"
            rows="3"
          ></textarea>

          <div class="row mb-2">
            <div class="col-6">
              <div class="form-check">
                <input
                  class="form-check-input"
                  v-model="this.createJoinModal.public"
                  type="checkbox"
                  value=""
                  id="checkDefault"
                />
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
          <button
            class="button mt-1"
            style="width: 100%"
            @click="createServer()"
          >
            Create Server
          </button>
        </div>

        <div v-if="this.createJoinModal.tab == 1" style="padding: 10px">
          <p style="margin: 0" class="mb-2">
            Please enter the ID of the server you wish to join
          </p>
          <input
            class="text-input mb-2"
            placeholder="Server ID"
            style="width: 100% !important; padding: 7px 10px"
          />

          <p style="color: red" v-if="this.createJoinModal.joinError != null">
            {{ this.createJoinModal.joinError }}
          </p>
          <button class="button mt-1" style="width: 100%">Join Server</button>
        </div>
      </div>
    </div>
  </div>
  <!-- END Create/Join Server Modal -->

  <!-- BEGIN Create Invite Modal -->
  <div
    class="modal fade"
    id="createInviteModal"
    tabindex="-1"
    aria-hidden="true"
  >
    <div
      class="modal-dialog modal-dialog-centered"
      style="max-width: 650px !important"
    >
      <div
        class="modal-content"
        style="
          background: var(--bg-0);
          padding: 10px;
          color: white;
          font-family: &quot;Ubuntu&quot;;
          max-width: 650px !important;
        "
      >
        <div class="row mb-2">
          <div class="col-6" style="margin: 0; padding: 0">
            <div
              :class="{
                'slider-tab': true,
                active: this.createInviteModal.tab == 0,
              }"
              @click="this.createInviteModal.tab = 0"
            >
              Invite a Friend
            </div>
          </div>
          <div class="col-6" style="margin: 0; padding: 0">
            <div
              :class="{
                'slider-tab': true,
                active: this.createInviteModal.tab == 1,
              }"
              @click="this.createInviteModal.tab = 1"
            >
              Invite an Agent
            </div>
          </div>
        </div>

        <div style="padding: 10px" v-if="this.createInviteModal.tab == 0">
          <p style="text-align: center">Invite someone to join your server!</p>
          <p
            style="color: red"
            v-if="this.createInviteModal.createError != null"
          >
            {{ this.createInviteModal.createError }}
          </p>
          <div style="display: flex; flex-direction: row">
            <button
              class="button mt-1"
              style="width: 100%"
              @click="createInvite(this.currentServer.id)"
            >
              Create Invite
            </button>
            <button
              class="button mt-1"
              style="
                width: 100%;
                margin-left: 10px;
                background: var(--secondary);
              "
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
          </div>
        </div>

        <div style="padding: 10px" v-if="this.createInviteModal.tab == 1">
          <input
            class="text-input mb-2"
            placeholder="Agent Name"
            v-model="this.createInviteModal.agentName"
            style="width: 100%; padding: 7px 10px"
          />

          <textarea
            class="text-input mb-1"
            v-model="this.createInviteModal.agentPersonality"
            placeholder="Give your agent a personality"
            style="width: 100% !important; padding: 7px 10px"
            rows="3"
          ></textarea>

          <select
            class="form-select text-input"
            v-model="this.createInviteModal.agentModel"
          >
            <option value="" selected disabled>Select a model type</option>
            <option value="llama">Llama 3</option>
            <option value="mistral">Mistral</option>
            <option value="gemma">Gemma</option>
          </select>

          <div style="display: flex; flex-direction: row">
            <button
              class="button mt-3"
              style="width: 100%"
              @click="createAgent()"
            >
              Create Agent
            </button>
            <button
              class="button mt-3"
              style="
                width: 100%;
                margin-left: 10px;
                background: var(--secondary);
              "
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- END Create Invite Modal -->

  <!-- BEGIN Update Agent Modal -->
  <div
    class="modal fade"
    id="updateAgentInfoModal"
    tabindex="-1"
    aria-hidden="true"
  >
    <div
      class="modal-dialog modal-dialog-centered"
      style="max-width: 650px !important"
    >
      <div
        class="modal-content"
        style="
          background: var(--bg-0);
          padding: 10px;
          color: white;
          font-family: &quot;Ubuntu&quot;;
          max-width: 650px !important;
        "
      >
        <div class="row mb-2">
          <div class="col-12" style="margin: 0; padding: 0">
            <div class="slider-tab active">Update Agent</div>
          </div>
        </div>

        <div style="padding: 10px">
          <input
            class="text-input mb-2"
            placeholder="Agent Name"
            v-model="this.updateAgentModal.agentName"
            style="width: 100%; padding: 7px 10px"
          />

          <textarea
            class="text-input mb-1"
            v-model="this.updateAgentModal.agentPersonality"
            placeholder="Give your agent a personality"
            style="width: 100% !important; padding: 7px 10px"
            rows="3"
          ></textarea>

          <select
            class="form-select text-input"
            v-model="this.updateAgentModal.agentModel"
          >
            <option value="" selected disabled>Select a model type</option>
            <option value="llama">Llama 3</option>
            <option value="mistral">Mistral</option>
            <option value="gemma">Gemma</option>
          </select>

          <div style="display: flex; flex-direction: row">
            <button
              class="button mt-3"
              style="width: 100%"
              @click="updateAgent()"
            >
              Update Agent
            </button>
            <button
              class="button mt-3"
              style="
                width: 100%;
                margin-left: 10px;
                background: var(--secondary);
              "
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- END Update Agent Modal -->

  <div class="loading" v-if="!this.ready || this.needsUsername">
    <img :src="logo" style="width: 200px" /> <br />

    <div
      class="spinner-border custom-spinner"
      role="status"
      v-if="!this.ready && !this.needsUsername"
    >
      <span class="visually-hidden">Loading...</span>
    </div>

    <div v-if="this.needsUsername" style="text-align: center; width: 400px">
      <h3 style="margin: 0">Welcome to SmallTalk, {{ user.given_name }}!</h3>
      <p style="margin: 0; margin-top: 15px; font-size: 18px">
        We're excited you're here. We need a name to call you in order to get
        started.
      </p>
      <input
        v-model="desiredDisplayName"
        class="text-input"
        placeholder="Display Name"
        style="width: 100% !important; padding: 7px 10px; margin-top: 25px"
      />
      <input
        v-model="desiredUsername"
        class="text-input"
        placeholder="Username"
        style="width: 100% !important; padding: 7px 10px; margin-top: 10px"
      />
      <p
        style="margin: 0; color: red; margin-top: 15px"
        v-if="this.hasUsernameError"
      >
        Sorry, that username is already taken.
      </p>
      <button
        class="button"
        style="margin-top: 25px; width: 300px"
        @click="submitUsername()"
      >
        Let's Go!
      </button>
    </div>
  </div>

  <div class="main" v-if="this.ready && !this.needsUsername">
    <div class="head-nav">
      <img :src="logo" style="width: 125px" />
      <input
        class="text-input"
        placeholder="Search your messages..."
        v-model="this.search.input"
        @keyup.enter="searchMessages()"
        style="width: 400px !important; padding: 7px 10px"
      />
    </div>
    <div class="top-bar">
      {{
        this.currentServer.name ||
        this.currentServer.charAt(0).toUpperCase() + this.currentServer.slice(1)
      }}
    </div>
    <div class="app-window">
      <div style="display: flex; flex-direction: column">
        <div
          style="
            display: flex;
            flex-direction: row;
            flex: 1;
            overflow-y: scroll;
            overflow-x: hidden;
          "
        >
          <div class="server-sidebar">
            <ServerBar
              :servers="this.userServers"
              :currentServer="this.currentServer"
              @update-currentServer="
                this.currentServer = $event;
                this.currentChannel = null;
              "
              @open-modal="openCreateJoinModal"
            />
          </div>
          <div class="left-sidebar">
            <ChannelBar
              ref="channelBar"
              :currentServer="this.currentServer"
              :currentChannel="this.currentChannel"
              :agents="this.userAgents"
              :currentSearchTab="this.search.tab"
              @update-currentChannel="this.currentChannel = $event"
              @update-chatChannels="this.chatChannels = $event"
              @update-search-tab="this.search.tab = $event"
              @wake-agent="wakeAgent"
              @open-agent-modal="openUpdateAgentModal"
              @sleep-agent="sleepAgent"
            />
          </div>
        </div>

        <div class="connection-status">
          <div class="overall-status">
            <div style="display: flex; align-items: center">
              <div
                :class="{
                  'spinner-grow': true,
                  'text-warning': this.ws_info.connectionState == null,
                  'text-success': this.ws_info.connectionState == 2,
                }"
                role="status"
                style="width: 12px; height: 12px; margin-right: 7px"
              ></div>
              <template v-if="this.ws_info.connectionState == null"
                >Connecting to real-time services...</template
              >
              <template v-if="this.ws_info.connectionState == 2"
                >Connceted to SmallTalk real-time services</template
              >
              <template v-if="this.ws_info.connectionState == 3"
                >Unable to connect to SmallTalk real-time services</template
              >
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
            <div
              class="account-center"
              data-bs-toggle="dropdown"
              aria-expanded="false"
              data-bs-auto-close="outside"
            >
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
            <div
              class="dropdown-menu p-3"
              style="
                width: 300px;
                background: #151626;
                border: 2px solid rgba(255, 255, 255, 0.12);
              "
            >
              <p
                style="
                  font-size: 20px;
                  color: #f2f2f2;
                  margin: 0;
                  font-weight: 700;
                "
              >
                {{ user.given_name }} {{ user.family_name }}
              </p>
              <p
                style="margin: 0; color: #f2f2f2; font-size: 15px"
                class="mb-3"
              >
                Signed in as <strong>{{ user.email }}</strong>
              </p>
              <button
                @click="logout()"
                type="button"
                class="btn btn-danger w-100"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        class="main-content"
        v-if="this.currentServer != 'home' && this.currentServer != 'search'"
      >
        <ChatWindow
          :currentChannel="this.currentChannel"
          :currentUser="this.userInfo"
          :pusher="this.ws_info.pusher"
        />
      </div>

      <div
        class="right-sidebar"
        v-if="this.currentServer != 'home' && this.currentServer != 'search'"
      >
        <!-- <MemberBar :server="this.currentServer" /> -->
        <div
          style="
            flex: 1;
            overflow-y: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
          "
          v-if="this.currentServerMembers.loading"
        >
          <div class="spinner-border custom-spinner" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div
          style="flex: 1; overflow-y: scroll"
          v-if="!this.currentServerMembers.loading"
        >
          <div
            style="
              display: flex;
              flex-direction: row;
              align-items: center;
              justify-content: space-between;
              margin-bottom: 10px;
            "
          >
            <p style="margin: 0; font-weight: 700">Members</p>
            <button
              class="button"
              data-bs-toggle="modal"
              data-bs-target="#createInviteModal"
              style="
                padding: 5px 10px;
                background-color: rgb(68, 69, 82);
                font-size: 12px;
              "
              @click="openCreateInviteModal(0)"
            >
              <i class="bi bi-plus"></i>
            </button>
          </div>

          <template v-for="member in this.currentServerMembers.members">
            <div
              style="
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                margin-bottom: 15px;
                align-items: center;
              "
            >
              <div
                style="
                  display: flex;
                  flex-direction: row;
                  justify-content: center;
                  align-items: center;
                "
              >
                <img :src="member.avatar_url" class="avatar" />
                <p style="margin: 0; margin-left: 15px" v-if="member.role != 0">
                  {{ member.displayName }}
                </p>
                <p
                  style="
                    margin: 0;
                    margin-left: 15px;
                    font-weight: 800;
                    color: #bb2d3c;
                  "
                  v-if="member.role == 0"
                >
                  {{ member.displayName }}
                </p>
              </div>
              <p
                style="margin: 0"
                v-if="
                  this.currentServerMembers.members.find(
                    (obj) => obj.id === this.userInfo.id,
                  ).role == 0 && member.id != this.userInfo.id
                "
              >
                <i class="bi bi-three-dots-vertical"></i>
              </p>
            </div>
          </template>

          <div
            style="
              display: flex;
              flex-direction: row;
              align-items: center;
              justify-content: space-between;
              margin-bottom: 10px;
            "
          >
            <p style="margin: 0; font-weight: 700">Agents</p>
            <button
              class="button"
              data-bs-toggle="modal"
              data-bs-target="#createInviteModal"
              style="
                padding: 5px 10px;
                background-color: rgb(68, 69, 82);
                font-size: 12px;
              "
              @click="openCreateInviteModal(1)"
            >
              <i class="bi bi-plus"></i>
            </button>
          </div>

          <template v-if="this.currentServerMembers.agents.length == 0">
            <div
              style="
                width: 100%;
                height: 150px;
                display: flex;
                align-items: center;
                justify-content: center;
              "
            >
              <div
                style="
                  text-align: center;
                  width: 200px;
                  color: var(--secondary);
                "
              >
                There are no agents in this server
              </div>
            </div>
          </template>
          <template v-for="agent in this.currentServerMembers.agents">
            <div
              style="
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                margin-bottom: 15px;
                align-items: center;
              "
            >
              <div
                style="
                  display: flex;
                  flex-direction: row;
                  justify-content: center;
                  align-items: center;
                "
              >
                <div
                  :class="{
                    avatar: true,
                    'agent-llama': agent.model == 'llama3.2',
                    'agent-gemma': agent.model == 'gemma3',
                  }"
                  v-if="[1, 3].includes(agent.status)"
                >
                  <i class="bi bi-stars"></i>
                </div>
                <div
                  class="spinner-border custom-spinner"
                  v-if="[0, 2].includes(agent.status)"
                >
                  <span class="visually-hidden">Loading...</span>
                </div>
                <div style="margin-left: 15px">
                  <p style="margin: 0">{{ agent.name }} ({{ agent.model }})</p>
                  <p
                    style="margin: 0; font-size: 12px"
                    v-if="agent.status == 0"
                  >
                    Initializing...
                  </p>
                  <p
                    style="margin: 0; font-size: 12px; color: green"
                    v-if="agent.status == 1"
                  >
                    Ready
                  </p>
                  <p
                    style="margin: 0; font-size: 12px"
                    v-if="agent.status == 2"
                  >
                    Typing in {{ getTypingChannel(agent.typingIn) }}...
                  </p>
                  <p
                    style="margin: 0; font-size: 12px"
                    v-if="agent.status == 3"
                  >
                    Sleeping
                  </p>
                </div>
              </div>
              <div class="dropdown">
                <p
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                  style="margin: 0"
                  v-if="agent.user_id == this.userInfo.id"
                >
                  <i class="bi bi-three-dots-vertical"></i>
                </p>

                <ul
                  class="dropdown-menu"
                  style="
                    width: 300px;
                    background: #151626;
                    border: 2px solid rgba(255, 255, 255, 0.12);
                  "
                >
                  <li>
                    <a
                      class="dropdown-item"
                      v-if="agent.status == 3"
                      @click="openUpdateAgentModal(agent)"
                      >Edit agent settings</a
                    >
                  </li>
                  <li>
                    <a
                      class="dropdown-item"
                      v-if="agent.status == 3"
                      @click="wakeAgent(agent.id)"
                      >Wake agent</a
                    >
                  </li>
                  <li>
                    <a
                      class="dropdown-item"
                      style="color: #bb2d3c !important"
                      v-if="agent.status != 3"
                      @click="sleepAgent(agent.id)"
                      >Send agent to sleep</a
                    >
                  </li>
                </ul>
              </div>
            </div>
          </template>
        </div>
      </div>

      <div class="home-content" v-if="this.currentServer == 'home'">
        <div style="text-align: center">
          <img :src="logoFlat" style="width: 250px" /> <br />
          <p
            style="margin: 0; font-size: 32px; font-weight: 0; margin-top: 25px"
          >
            <strong>Welcome, @{{ userInfo.username }}!</strong>
          </p>
          <p style="margin: 0; font-size: 28px; font-weight: 0">
            Select a server to get started
          </p>

          <div
            style="
              display: flex;
              flex-direction: row;
              align-items: center;
              justify-content: center;
              margin-top: 25px;
            "
          >
            <div
              style="
                width: 150px;
                display: flex;
                justify-content: center;
                align-items: center;
              "
            >
              <div>
                <p style="margin: 0; color: #674ea7; font-size: 45px">
                  {{ this.userStats.messages }}
                </p>
                <p>message(s) sent</p>
              </div>
            </div>
            <div
              style="
                width: 150px;
                height: 100px;
                display: flex;
                justify-content: center;
                align-items: center;
              "
            >
              <div>
                <p style="margin: 0; color: #674ea7; font-size: 45px">
                  {{ this.userStats.agents }}
                </p>
                <p>agent(s)</p>
              </div>
            </div>
            <div
              style="
                width: 150px;
                height: 100px;
                display: flex;
                justify-content: center;
                align-items: center;
              "
            >
              <div>
                <p style="margin: 0; color: #674ea7; font-size: 45px">
                  {{ this.userStats.servers }}
                </p>
                <p>server(s) owned</p>
              </div>
            </div>
          </div>

          <div style="margin-top: 25px">
            <button
              class="button"
              style="width: 300px; background: #444552"
              data-bs-toggle="modal"
              data-bs-target="#createJoinModal"
              @click="this.createJoinModal.tab = 0"
            >
              Create a Server
            </button>
            <button
              class="button"
              style="width: 300px; background: #444552; margin-left: 15px"
              data-bs-toggle="modal"
              data-bs-target="#createJoinModal"
              @click="this.createJoinModal.tab = 1"
            >
              Join a Server
            </button>
          </div>
        </div>
      </div>

      <div class="home-content" v-if="this.currentServer == 'search'">
        <div style="text-align: center" v-if="this.search.tab == 0">
          <h1
            style="
              font-size: 32px;
              font-weight: 600;
              color: white;
              margin-bottom: 20px;
            "
          >
            What are you trying to find today?
          </h1>
          <input
            class="text-input"
            placeholder="Search your messages..."
            v-model="this.search.input"
            @keyup.enter="searchMessages()"
            style="width: 800px !important; padding: 7px 10px; font-size: 25px"
          />
        </div>

        <div
          style="
            width: 100%;
            height: 100%;
            overflow-y: scroll !important;
            padding: 10px;
          "
          v-if="
            this.search.tab == 1 &&
            this.search.results != null &&
            this.search.loading != true
          "
        >
          <input
            class="text-input"
            placeholder="Search your messages..."
            v-model="this.search.input"
            @keyup.enter="searchMessages()"
            style="width: 100% !important; padding: 7px 10px"
          />
          <p class="my-2" style="color: white">
            Found <strong>{{ this.search.results.count }} results</strong> to
            your query
          </p>
          <ol class="message-list">
            <template v-for="message in this.search.results.results">
              <li class="message-list-item">
                <Message :message="message" :isMe="false" />
              </li>
            </template>
          </ol>
        </div>

        <div
          v-if="
            this.search.tab == 1 &&
            this.search.results == null &&
            this.search.loading == false
          "
        >
          Please submit a search query before viewing results
        </div>

        <div v-if="this.search.tab == 1 && this.search.loading == true">
          <div class="spinner-border custom-spinner" role="status">
            <span class="visually-hidden">Loading...</span>
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
        if (response.status == 201) {
          this.userServers.push(response.data);
          bootstrap.Modal.getInstance(
            document.getElementById("createJoinModal"),
          ).hide();
        } else {
          this.createJoinModal.createError = response.data["message"];
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
        if (response.status == 201) {
          this.userServers.push(response.data);
          bootstrap.Modal.getInstance(
            document.getElementById("createJoinModal"),
          ).hide();
        } else {
          this.createJoinModal.createError = response.data["message"];
        }
      },
      ws_info: {
        connectionState: null,
        latency: null,
        pusher: null,
      },
      agent_control: null,
      createJoinModal: {
        tab: 0,
        name: null,
        description: null,
        icon_url: null,
        public: false,
        createError: null,
        joinError: null,
      },
      createInviteModal: {
        createError: null,
        agentName: null,
        agentPersonality: null,
        agentModel: null,
        tab: 0,
      },
      updateAgentModal: {
        agentId: null,
        agentName: null,
        agentModel: null,
        agentPersonality: null,
      },
      userServers: [],
      chatChannels: [],
      currentServer: "home",
      currentServerMembers: {
        loading: false,
        members: [],
        agents: [],
      },
      currentChannel: null,
      user,
      userInfo: null,
      userStats: null,
      userAgents: [],
      needsUsername: false,
      hasUsernameError: false,
      isAuthenticated,
    };
  },
  async mounted() {
    await this.loadUserInfo();
    await this.loadUserAgents();
    await this.loadUserServers();
    this.ready = true;
    this.initPusherConnection();
  },
  watch: {
    currentServer(newServer) {
      if (newServer !== "home" && newServer !== "search") {
        this.fetchServerMembers(newServer.id);
      }
    },
  },
  methods: {
    async loadUserAgents() {
      let response = await this.$store.dispatch("agent/listOwnedAgents", {
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      this.userAgents = response.data;
    },
    async loadUserInfo() {
      this.userInfo = await this.$store.dispatch("user/getUserInfo", {
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      this.userStats = await this.$store.dispatch("user/getUserStats", {
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
          iconUrl: this.createJoinModal.icon_url,
          public: this.createJoinModal.public == "true",
        },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      if (response.status && response.status != 201) {
        this.createJoinModal.createError = response.data.message;
      } else {
        this.userServers.push(response.data);
        this.userServers.sort((a, b) => a.name.localeCompare(b.name));
        this.currentServer = response.data;
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("createJoinModal"),
        );
        modal.hide();
      }
    },
    async createAgent() {
      let response = await this.$store.dispatch("agent/createAgent", {
        serverId: this.currentServer.id,
        payload: {
          name: this.createInviteModal.agentName,
          personality: this.createInviteModal.agentPersonality,
          model: this.createInviteModal.agentModel,
        },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      if (response.status && response.status != 201) {
        this.createJoinModal.createError = response.data.message;
      } else {
        this.currentServerMembers.agents.push(response.data);
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("createInviteModal"),
        );
        modal.hide();
      }
    },
    async updateAgent() {
      let response = await this.$store.dispatch("agent/updateAgent", {
        agentId: this.updateAgentModal.agentId,
        payload: {
          name: this.updateAgentModal.agentName,
          personality: this.updateAgentModal.agentPersonality,
          model: this.updateAgentModal.agentModel,
        },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      if (response.status && response.status != 200) {
        alert(response.data.message);
      } else {
        let serverAgent = this.currentServerMembers.agents.find(
          (obj) => obj.id === this.updateAgentModal.agentId,
        );
        if (serverAgent) {
          Object.assign(serverAgent, response.data);
        }

        let userAgent = this.userAgents.find(
          (obj) => obj.id === this.updateAgentModal.agentId,
        );
        if (userAgent) {
          Object.assign(userAgent, response.data);
        }

        const modal = bootstrap.Modal.getInstance(
          document.getElementById("updateAgentInfoModal"),
        );
        modal.hide();
      }
    },
    async wakeAgent(agentId) {
      await this.$store.dispatch("agent/wakeAgent", {
        agentId: agentId,
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
    },
    async sleepAgent(agentId) {
      await this.$store.dispatch("agent/sleepAgent", {
        agentId: agentId,
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
    },
    async fetchServerMembers(serverId) {
      this.currentServerMembers.loading = true;

      let member_response = await this.$store.dispatch(
        "server/listServerMembers",
        {
          serverId: serverId,
          accessToken: await this.$auth0.getAccessTokenSilently(),
        },
      );
      if (member_response.status == 200) {
        this.currentServerMembers.members = member_response.data;
      }

      let agent_response = await this.$store.dispatch(
        "server/listServerAgents",
        {
          serverId: serverId,
          accessToken: await this.$auth0.getAccessTokenSilently(),
        },
      );
      if (agent_response.status == 200) {
        this.currentServerMembers.agents = agent_response.data;
      }

      this.currentServerMembers.loading = false;
    },
    initPusherConnection() {
      Pusher.logToConsole = true;

      this.ws_info.pusher = new Pusher(import.meta.env.VITE_PUSHER_KEY, {
        cluster: "us3",
      });

      this.ws_info.pusher.connection.bind("connected", () => {
        this.ws_info.connectionState = 2;
        const pingTime = Date.now();
        const testChannel = this.ws_info.pusher.subscribe(
          "public-latency-test",
        );
        testChannel.bind("pusher:subscription_succeeded", () => {
          const pongTime = Date.now();
          this.ws_info.latency = pongTime - pingTime;
        });
      });
      this.ws_info.pusher.connection.bind("unavailable", () => {
        this.ws_info.connectionState = 3;
      });

      this.agent_control = this.ws_info.pusher.subscribe("agent-control");
      this.agent_control.bind("status-change", (data) => {
        const serverAgent = this.currentServerMembers.agents.find(
          (obj) => obj.id === data.agentId,
        );
        if (serverAgent != null) {
          serverAgent.status = data.status;
          if ("typingIn" in data) {
            serverAgent.typingIn = data.typingIn;
          }
        }

        const userAgent = this.userAgents.find(
          (obj) => obj.id === data.agentId,
        );
        if (serverAgent != null) {
          userAgent.status = data.status;
        }
      });
    },
    openCreateJoinModal() {
      Object.assign(this.createJoinModal, {
        name: null,
        description: null,
        icon_url: null,
        public: false,
        createError: null,
        tab: 0,
      });
    },
    openCreateInviteModal(tab = 0) {
      Object.assign(this.createInviteModal, {
        name: null,
        maxUses: null,
        createError: null,
        agentName: null,
        agentModel: null,
        tab: tab,
      });
    },
    openUpdateAgentModal(agent) {
      let modelMap = {
        "llama3.2": "llama",
        gemma3: "gemma",
        mistral: "mistral",
      };

      this.updateAgentModal.agentId = agent.id;
      this.updateAgentModal.agentName = agent.name;
      this.updateAgentModal.agentPersonality = agent.personality;
      this.updateAgentModal.agentModel = modelMap[agent.model];

      const modal = new bootstrap.Modal(
        document.getElementById("updateAgentInfoModal"),
      );
      modal.show();
    },
    async createInvite(serverId) {
      let response = await this.$store.dispatch("server/createInvite", {
        payload: {
          serverId: serverId,
        },
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });

      if (response.status && response.status != 201) {
        this.createInviteModal.createError = response.data.message;
      } else {
        const inviteLink = `${window.location.origin}/invite/${response.data.invite_code}`;
        await navigator.clipboard.writeText(inviteLink);
        alert("Invite link copied to clipboard!");
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("createInviteModal"),
        );
        modal.hide();
      }
    },
    getTypingChannel(channelId) {
      const channel = this.chatChannels.find((obj) => obj.id === channelId);
      if (channel == null) return "a different server";
      return channel.name;
    },
    async searchMessages() {
      this.currentServer = "search";
      this.search.tab = 1;
      this.search.loading = true;
      let response = await this.$store.dispatch("message/searchMessages", {
        query: this.search.input,
        accessToken: await this.$auth0.getAccessTokenSilently(),
      });
      if (response.status == 200) {
        this.search.results = response.data;
      }
      this.search.loading = false;
    },
  },
};
</script>
