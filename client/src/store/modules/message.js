import Api from "@/services/api";

export default {
    namespaced: true,
    state: {
    },
    mutations: {
    },
    actions: {
        async fetchMessages({ commit }, data) {
            try {
                let response = await Api().get(
                    `channels/${data.payload.channelId}/messages`,
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
        async postMessage({ commit }, data) {
            console.log("Posting message with data:", data);
            try {
                let response = await Api().post(
                    `channels/${data.payload.channelId}/messages`,
                    {
                        content: data.payload.content,
                        reply_to_id: data.payload.replyToMessageId
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
        async searchMessages({ commit }, data) {
            try {
                let response = await Api().post(
                    `messages/search`,
                    {
                        query: data.query,
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
        }
    },
    getters: {
    }
}
