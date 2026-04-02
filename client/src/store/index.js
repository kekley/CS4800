import { createStore } from 'vuex'

import serverModule from './modules/server';
import userModule from './modules/user';

export default createStore({
    modules: {
        server: serverModule,
        user: userModule
    },
    state: {
        user: null
    },
    mutations: {
        SET_USER(state,user) {
            state.user = user;
        }
    },
    actions: {

    },
    getters: {
        
    }
});