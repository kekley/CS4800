import Api from "@/services/api";

export default {
    namespaced: true,
    state: {
    },
    mutations: {
    },
    actions: {
        async getUserInfo({commit}, data) {
            try {
                let response = await Api().get('users/self', {
                    headers: {
                        'Authorization': `Bearer ${data.accessToken}`
                    }
                });
                return response.data;
            } catch(error) {
                return error.response;
            }
        },
        async updateUserInfo({commit}, data) {
            try {
                let response = await Api().post('users/self', data.updates, {
                    headers: {
                        'Authorization': `Bearer ${data.accessToken}`
                    }
                });
                return response.status;
            } catch(error) {
                return error.response;
            }
        },
        async getUserStats({commit}, data) {
            try {
                let response = await Api().get('users/self/stats', {
                    headers: {
                        'Authorization': `Bearer ${data.accessToken}`
                    }
                });
                return response.data;
            } catch(error) {
                return error.response;
            }
        }
    },
    getters: {
    }
}