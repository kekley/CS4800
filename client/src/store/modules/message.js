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
                const headers = {
                    'Authorization': `Bearer ${data.accessToken}`
                };
                let body = {
                    content: data.payload.content,
                    reply_to_id: data.payload.replyToMessageId
                };

                if (data.payload.files && data.payload.files.length > 0) {
                    body = new FormData();
                    body.append("content", data.payload.content || "");

                    if (data.payload.replyToMessageId != null) {
                        body.append("reply_to_id", data.payload.replyToMessageId);
                    }

                    data.payload.files.forEach((file) => {
                        body.append("files", file);
                    });
                }

                let response = await Api().post(
                    `channels/${data.payload.channelId}/messages`,
                    body,
                    {
                        headers
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
