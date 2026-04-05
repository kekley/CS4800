<script setup>
</script>

<template>
    <div class="server-creation-popup">
        <div v-if="!hasServerCreationError" class="popup-content">
            <h3 style="margin: 0;">Create a Server</h3>
            <input class="text-input" v-model="newServerName" placeholder="Server Name"
                style="width: 100% !important; padding: 7px 10px; margin-top: 25px;" />
            <input class="text-input" v-model="newServerDescription" placeholder="Server Description"
                style="width: 100% !important; padding: 7px 10px; margin-top: 10px;" />
            <input class="text-input" v-model="newServerIconUrl" placeholder="Icon URL"
                style="width: 100% !important; padding: 7px 10px; margin-top: 10px;" />
            <button class="button" style="margin-top: 25px; width: 100%;" @click="createServer">Create</button>
            <button class="button" style="margin-top: 10px; width: 100%; background: #444552;"
                @click="$emit('serverCreateCancel')">Cancel</button>
        </div>
        <div v-if="hasServerCreationError" class="popup-content">
            <h3 style="margin: 0;">Create a Server</h3>
            <p style="color: red; margin: 0; margin-top: 15px;">{{ serverCreationErrorMessage }}</p>
            <button class="button" style="margin-top: 25px; width: 100%;"
                @click="hasServerCreationError = false; serverCreationErrorMessage = null">Try Again</button>
            <button class="button" style="margin-top: 10px; width: 100%; background: #444552;"
                @click="$emit('serverCreateCancel')">Cancel</button>
        </div>
    </div>

</template>

<script>
export default {
    name: "CreateServer",
    data() {
        return {
            hasServerCreationError: false,
            serverCreationErrorMessage: null,
            newServerName: null,
            newServerDescription: null,
            newServerIconUrl: null,
        }
    },
    methods: {
        async createServer() {
            let response = await this.$store.dispatch('server/createServer', {
                name: this.newServerName,
                description: this.newServerDescription,
                iconUrl: this.newServerIconUrl,
                accessToken: await this.$auth0.getAccessTokenSilently()
            });
            if (response.status == 201) {
                this.isServerCreating = false;
                this.$emit('serverCreated');
            } else {
                this.hasServerCreationError = true;
                this.serverCreationErrorMessage = response.data.message;
            }
        },
    }
}
</script>