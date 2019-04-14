import Vue from 'vue';

import axios from 'axios';
import VueAxios from 'vue-axios';

import VueRouter from 'vue-router';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faTimes, faEdit, faSave, faPlusSquare, faArrowUp, faArrowDown } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import Cookies from 'js-cookie';

import './../node_modules/bulma/css/bulma.css';

import App from './App.vue';

Vue.config.productionTip = false;

// Fontawesome stuff
library.add(faTimes);
library.add(faEdit);
library.add(faSave);
library.add(faPlusSquare);
library.add(faArrowUp);
library.add(faArrowDown);
Vue.component('font-awesome-icon', FontAwesomeIcon);


//Vue-router stuff
Vue.use(VueRouter);

const routes = [
    {
        path: '/login',
        component: require('./components/Login.vue').default,
        name: 'login',
        meta: {title: 'PACT | Login'},
    },
    {
        path: '/characters',
        component: require('./components/Characters.vue').default,
        name: 'characters',
        meta: {title: 'PACT | characters'},
    },
    {
        path: '/characters/create',
        component: require('./components/CharacterCreate.vue').default,
        name: 'character-create',
        meta: {title: 'PACT | character create'},
    },
    {
        path: '/characters/:uuid',
        component: require('./components/Character.vue').default,
        name: 'character',
        meta: {title: 'PACT | character'},
    },
    {
        path: '/characters/:uuid/edit',
        component: require('./components/CharacterEdit.vue').default,
        name: 'character-edit',
        meta: {title: 'PACT | character edit'},
    },
    {
        path: '/encounters',
        component: require('./components/Encounters.vue').default,
        name: 'encounters',
        meta: {title: 'PACT | encounters'},
    },
    {
        path: '/encounters/:uuid',
        component: require('./components/Encounter.vue').default,
        name: 'encounter',
        meta: {title: 'PACT | encounter'},
    },
    {
        path: '/encounters/create',
        component: require('./components/EncounterCreate.vue').default,
        name: 'encounter-create',
        meta: {title: 'PACT | encounter create'},
    },
]

const router = new VueRouter({
    routes: routes
});

router.beforeEach((to, from, next) => {
    document.title = to.meta.title
    next()
});

// Axios stuff
Vue.use(VueAxios, axios)

Vue.axios.interceptors.response.use((response) => {
    return response
}, (error) => {
    if (error.response.status === 401 || error.response.status === 403) {
        router.push({ name: 'login', params: { nextUrl: window.location.hash.split('#')[1] }});
    }
    return Promise.reject(error)
});

Vue.axios.interceptors.request.use(function (config) {
    const csrf = Cookies.get('csrftoken');

    if (csrf != null) {
        config.headers['X-CSRFToken'] = csrf;
    }

    return config;
}, function (err) {
    return Promise.reject(err);
});

new Vue({
    router,
    el: '#app',
    render: h => h(App)
});
