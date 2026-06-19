import Api from "@/services/api";

export default {
  namespaced: true,
  state: {},
  mutations: {},
  actions: {
    async createAgent({ commit }, data) {
      try {
        let response = await Api().post(
          `agents/create/${data.serverId}`,
          data.payload,
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
    async updateAgent({ commit }, data) {
      try {
        let response = await Api().put(
          `agents/${data.agentId}`,
          data.payload,
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
    async wakeAgent({ commit }, data) {
      try {
        let response = await Api().post(
          `agents/${data.agentId}/wake`,
          null,
          {
            headers: {
              Authorization: `Bearer ${data.accessToken}`,
            },
          },
        );
        return response.status == 204;
      } catch (error) {
        return error.response;
      }
    },
    async sleepAgent({ commit }, data) {
      try {
        let response = await Api().post(
          `agents/${data.agentId}/sleep`,
          null,
          {
            headers: {
              Authorization: `Bearer ${data.accessToken}`,
            },
          },
        );
        return response.status == 204;
      } catch (error) {
        return error.response;
      }
    },
    async listOwnedAgents({ commit }, data) {
      try {
        let response = await Api().get(
          `agents/list`,
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
    async assocAgent({ commit }, data) {
      try {
        let response = await Api().put(
          `agents/${data.agentId}/assoc/${data.serverId}`,
          null,
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
