import { createStore } from 'vuex'

import serverModule from './modules/server';
import userModule from './modules/user';
<<<<<<< HEAD
import agentModule from './modules/agent';
import channelModule from './modules/channel';
import messageModule from './modules/message';
=======
import channelModule from './modules/channel';
>>>>>>> 264d9ca (add channel creation modal)

export default createStore({
    modules: {
        server: serverModule,
        user: userModule,
<<<<<<< HEAD
        agent: agentModule,
        channel: channelModule,
        message: messageModule
=======
        channel: channelModule
>>>>>>> 264d9ca (add channel creation modal)
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