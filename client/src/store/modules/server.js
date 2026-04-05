import Api from "@/services/api";

export default {

    namespaced: true,
    state: {},
    mutations: {},
    actions: {
        async listUserServers({ commit }, data) {
            try {
                let response = await Api().get("servers/self/list", {
                    headers: {
                        Authorization: `Bearer ${data.accessToken}`,
                    },
                });
                return response.data;
            } catch (error) {
                return error.response;
            }
        },
        async createServer({ commit }, data) {
            try {
                let response = await Api().post(
                    "servers/create",
                    {
                        name: data.payload.name,
                        description: data.payload.description,
                        icon_url: data.payload.iconUrl,
                        is_private: data.payload.isPrivate,
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${data.accessToken}`,
                        },
                        async createServer({ commit }, data) {
                            try {
                                let response = await Api().post('servers/create', data.payload, {
                                    headers: {
                                        'Authorization': `Bearer ${data.accessToken}`
                                    }
                                });
                                return response;
                            } catch (error) {
                                return error.response;
                            }
                        }
                    },
                    async joinServer({ commit }, data) {
                    try {
                        let response = await Api().get(
                            `servers/join/${data.payload.inviteCode}`,
                            {
                                headers: {
                                    Authorization: `Bearer ${data.accessToken}`,
                                },
                            },
                        );
                        return response;
                    } catch(error) {
                        return error.response;
                    }
                },
                    async listServerMembers({ commit }, data) {
                    try {
                        let response = await Api().get(
                            `servers/${data.serverId}/members`,
                            {
                                headers: {
                                    Authorization: `Bearer ${data.accessToken}`,
                                },
                            },
                        );
                        return response;
                    } catch(error) {
                        return error.response;
                    }
                },
                    async listServerAgents({ commit }, data) {
                    try {
                        let response = await Api().get(
                            `servers/${data.serverId}/agents`,
                            {
                                headers: {
                                    Authorization: `Bearer ${data.accessToken}`,
                                },
                            },
                        );
                        return response;
                    } catch(error) {
                        return error.response;
                    }
                }
    },
            getters: { },
        };
