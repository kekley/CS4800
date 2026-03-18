<script setup>
import "../assets/server-bar.css";

import { ref, computed } from "vue";

let servers = [1, 2, 3, 4, 5];

</script>

<template>
  <div class="server-bar">
    <div class="server-list">
      <template v-for="server in servers">
        <div class="server-thumb">
          <img class="server-img" src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png">
        </div>
      </template>
      <div class="server-thumb">
          <div class="add-server">
            <i class="bi bi-plus"></i>
          </div>
        </div>
    </div>
    <div class="user-avatar">
      <img class="profile" src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png">
    </div>
  </div>
</template>
