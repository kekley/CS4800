import Api from "@/services/api";

export default {
    namespaced: true,
    state: {
    },
    mutations: {
    },
    actions: {
        async listUserServers({commit}, data) {
            try {
                let response = await Api().get('servers/self/list', {
                    headers: {
                        'Authorization': `Bearer ${data.accessToken}`
                    }
                });
                return response.data;
            } catch(error) {
                return error.response;
            }
        },
    },
    getters: {
    }
}