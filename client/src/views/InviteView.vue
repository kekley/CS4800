<template>
    <div class="invite-view">
        <div class="invite-card">
            <h2>Joining server...</h2>

            <div v-if="status === 'loading'" class="invite-status">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p>Joining server...</p>
            </div>

            <div v-if="status === 'success'" class="invite-status">
                <p class="text-success">Invite accepted! Redirecting you now...</p>
                <button class="button" @click="goToApp">Go to App</button>
            </div>

            <div v-if="status === 'error'" class="invite-status">
                <p class="text-danger">{{ errorMessage }}</p>
                <button class="button" @click="goToApp">Back to App</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuth0 } from '@auth0/auth0-vue';
import { useStore } from 'vuex';

const route = useRoute();
const router = useRouter();
const store = useStore();
const { getAccessTokenSilently } = useAuth0();

const status = ref('loading');
const errorMessage = ref('');

const inviteCode = route.params.code;

function goToApp() {
    router.push({ name: 'app' });
}

async function joinInvite() {
    if (!inviteCode) {
        status.value = 'error';
        errorMessage.value = 'No invite code was provided.';
        return;
    }

    try {
        const accessToken = await getAccessTokenSilently();
        const response = await store.dispatch('server/joinServer', {
            payload: { inviteCode },
            accessToken,
        });

        if (response?.status >= 200 && response?.status < 300) {
            status.value = 'success';
            setTimeout(() => {
                router.push({ name: 'app' });
            }, 1200);
            return;
        }

        status.value = 'error';
        errorMessage.value = response?.data?.message || 'Failed to join server with that invite.';
    } catch (err) {
        status.value = 'error';
        errorMessage.value = err?.message || 'There was a problem joining the invite.';
    }
}

onMounted(joinInvite);
</script>

<style scoped>
.invite-view {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    background: var(--bg-0);
}

.invite-card {
    width: min(520px, 100%);
    padding: 32px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(24, 27, 43, 0.95);
    border-radius: 16px;
    color: white;
    text-align: center;
}

.invite-status {
    margin-top: 24px;
}

.button {
    margin-top: 18px;
}
</style>
