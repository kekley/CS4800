<script setup>
import "../assets/server-bar.css";

import { ref, onMounted, watch } from "vue";

const props = defineProps({
  servers: {
    type: Object,
    required: true,
  },
  currentServer: {
    type: Object,
    required: true,
  },
});
const emit = defineEmits(["update-currentServer", "open-modal"]);

const initPopovers = () => {
  document
    .querySelectorAll('[data-bs-toggle="popover"]')
    .forEach((el) => new window.bootstrap.Popover(el));
};

onMounted(() => {
  initPopovers();
});

const selectServer = (server) => {
  emit("update-currentServer", server);
};

const openModal = () => {
  emit("open-modal", true);
};

watch(
  () => props.servers,
  async () => {
    setTimeout(initPopovers, 100);
  },
  { deep: true },
);
</script>

<template>
  <div class="server-bar">
    <div class="server-list">
      <div class="server-thumb">
        <div
          :class="{
            'server-icon': true,
            home: true,
            active: this.currentServer == 'home',
          }"
          data-bs-custom-class="custom-popover"
          data-bs-toggle="popover"
          data-bs-trigger="hover focus"
          data-bs-content="Home"
          @click="selectServer('home')"
        >
          <i class="bi bi-house"></i>
        </div>
      </div>

      <div class="server-thumb">
        <div
          :class="{
            'server-icon': true,
            home: true,
            active: this.currentServer == 'search',
          }"
          data-bs-custom-class="custom-popover"
          data-bs-toggle="popover"
          data-bs-trigger="hover focus"
          data-bs-content="Search"
          @click="selectServer('search')"
        >
          <i class="bi bi-search"></i>
        </div>
      </div>

      <template v-for="server in servers">
        <div class="server-thumb">
          <div
            :class="{
              'server-icon': true,
              active: this.currentServer.id == server.id,
            }"
            data-bs-custom-class="custom-popover"
            data-bs-toggle="popover"
            data-bs-trigger="hover focus"
            :data-bs-content="server.name"
            @click="selectServer(server)"
          >
            <template v-if="server.icon_url == null">
              {{ server.name[0] }}</template
            >
            <img
              :src="server.icon_url"
              v-if="server.icon_url != null"
              style="width: 100%; height: 100%; border-radius: 1000px"
            />
          </div>
        </div>
      </template>

      <div
        class="server-thumb"
        data-bs-toggle="modal"
        data-bs-target="#createJoinModal"
        @click="openModal()"
      >
        <div
          class="add-server"
          data-bs-custom-class="custom-popover"
          data-bs-toggle="popover"
          data-bs-trigger="hover focus"
          data-bs-content="Create or Join Server"
        >
          <i class="bi bi-plus"></i>
        </div>
      </div>
    </div>
  </div>
</template>
