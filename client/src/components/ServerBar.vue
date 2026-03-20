<script setup>
import "../assets/server-bar.css";

import { ref, onMounted } from "vue";

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
});

let servers = ["A", "B", "C", "D"];

onMounted(() => {
  document.querySelectorAll('[data-bs-toggle="popover"]')
    .forEach(el => new window.bootstrap.Popover(el));
});

</script>

<template>
  <div class="server-bar">
    <div class="server-list">
      <template v-for="server in servers">
        <div class="server-thumb">
          <div class="server-icon" data-bs-custom-class="custom-popover"
            data-bs-toggle="popover"
            data-bs-trigger="hover focus"
            :data-bs-content="'Example Server ' + server">
            {{ server }}
          </div>
        </div>
      </template>
      <div class="server-thumb">
          <div class="add-server" data-bs-custom-class="custom-popover"
            data-bs-toggle="popover"
            data-bs-trigger="hover focus"
            data-bs-content="Create or Add Server">
            <i class="bi bi-plus"></i>
          </div>
        </div>
    </div>
  </div>
</template>
