import { createStore } from 'vuex'

import serverModule from './modules/server';
import userModule from './modules/user';
import channelModule from './modules/channel';

export default createStore({
    modules: {
        server: serverModule,
        user: userModule,
        channel: channelModule
    },
    state: {
        user: null
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
        }
    },
    actions: {

    },
    getters: {

    }
});