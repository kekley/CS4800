import Api from "@/services/api";
import { join } from "lodash-es";

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
          },
        );
        return response;
      } catch (error) {
        return error.response;
      }
    },
    async createInvite({ commit }, data) {
      try {
        let response = await Api().post(
          `servers/${data.payload.serverId}/invite`,
          {
            name: data.payload.name,
            expires_after: data.payload.expiresAfter,
            max_uses: data.payload.maxUses,
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
      } catch (error) {
        return error.response;
      }
    }
  },
  getters: {},
};
