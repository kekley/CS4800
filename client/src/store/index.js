import { createStore } from 'vuex'

import serverModule from './modules/server';
import userModule from './modules/user';
import agentModule from './modules/agent';
import channelModule from './modules/channel';
import messageModule from './modules/message';

export default createStore({
    modules: {
        server: serverModule,
        user: userModule,
        agent: agentModule,
        channel: channelModule,
        message: messageModule
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
