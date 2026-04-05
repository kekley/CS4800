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
            name: data.name,
            description: data.description,
            icon_url: data.iconUrl,
            is_private: data.isPrivate,
          },
          {
            headers: {
              Authorization: `Bearer ${data.accessToken}`,
            },
          },
        );
        return response;
      } catch (error) {
        return error.response;
      }
    },
  },
  getters: {},
};

