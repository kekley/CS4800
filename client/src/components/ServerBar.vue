<script setup>
import "../assets/server-bar.css";

import { ref, onMounted } from "vue";

const props = defineProps({
  servers: {
    type: Object,
    required: true,
  },
  currentServer: {
    type: String,
    required: true,
  },
});
const emit = defineEmits(['update-currentServer']);

onMounted(() => {
  document.querySelectorAll('[data-bs-toggle="popover"]')
    .forEach(el => new window.bootstrap.Popover(el));
});

const selectServer = (serverId) => {
  emit('update-currentServer', serverId);
}

</script>

<template>
  <div class="server-bar">
    <div class="server-list">
        <div class="server-thumb">
            <div :class="{'server-icon': true, home: true, active: (this.currentServer == 'home')}" data-bs-custom-class="custom-popover"
              data-bs-toggle="popover"
              data-bs-trigger="hover focus"
              data-bs-content="Home"
              @click="selectServer('home')">
              <i class="bi bi-house"></i>
            </div>
        </div>

        <template v-for="server in servers">
          <div class="server-thumb">
            <div :class="{'server-icon': true, active: (this.currentServer == server)}" data-bs-custom-class="custom-popover"
              data-bs-toggle="popover"
              data-bs-trigger="hover focus"
              :data-bs-content="'Example Server ' + server"
              @click="selectServer(server)">
              {{ server }}
            </div>
          </div>
        </template>

        <div class="server-thumb" data-bs-toggle="modal" data-bs-target="#exampleModal">
            <div class="add-server" data-bs-custom-class="custom-popover"
              data-bs-toggle="popover"
              data-bs-trigger="hover focus"
              data-bs-content="Create or Join Server">
              <i class="bi bi-plus"></i>
            </div>
        </div>
    </div>
  </div>
</template>
