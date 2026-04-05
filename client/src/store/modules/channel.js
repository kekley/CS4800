import Api from "@/services/api";

export default {
    namespaced: true,
    state: {},
    mutations: {},
    actions: {
        async createChannel({ commit }, data) {
            console.log("Creating channel with data:", data);
            try {
                let response = await Api().post(
                    `servers/${data.payload.serverId}/channels`,
                    {
                        name: data.payload.name
                    },
                    {
                        headers: {
                            'Authorization': `Bearer ${data.accessToken}`
                        }
                    }
                );
                return response;
            } catch (error) {
                return error.response;
            }
        },
        async fetchChannels({ commit }, data) {
            try {
                let response = await Api().get(
                    `servers/${data.payload.serverId}/channels`,
                    {
                        headers: {
                            'Authorization': `Bearer ${data.accessToken}`
                        }
                    }
                );
                return response;
            } catch (error) {
                return error.response;
            }
        }
    }
}