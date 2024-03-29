import Vue from 'vue';

import axios from 'axios';
import VueAxios from 'vue-axios';

import VueRouter from 'vue-router';
import VModal from 'vue-js-modal'
import VueAutosize from 'vue-autosize';

import FlashMessage from '@smartweb/vue-flash-message';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faTimes, faEdit, faSave, faPlusSquare, faArrowUp, faArrowDown } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import Cookies from 'js-cookie';

require('@/main.scss');
import './../node_modules/vue2-autocomplete-js/dist/style/vue2-autocomplete.css';

import App from './App.vue';

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
        path: '/',
        component: () => import('./components/Overview.vue'),
        name: 'overview',
        meta: {title: 'PACT'}
    },
    {
        path: '/register',
        component: () => import('./components/Register.vue'),
        name: 'register',
        meta: {title: 'PACT | Sign up'}
    },
    {
        path: '/login',
        component: () => import('./components/Login.vue'),
        name: 'login',
        meta: {title: 'PACT | Login'},
    },
    {
        path: '/characters',
        component: () => import('./components/Characters.vue'),
        name: 'characters',
        meta: {title: 'PACT | characters'},
    },
    {
        path: '/characters/create',
        component: () => import('./components/CharacterCreate.vue'),
        name: 'character-create',
        meta: {title: 'PACT | character create'},
    },
    {
        path: '/characters/:uuid',
        component: () => import('./components/Character.vue'),
        name: 'character',
        meta: {title: 'PACT | character'},
    },
    {
        path: '/characters/:uuid/edit',
        component: () => import('./components/CharacterEdit.vue'),
        name: 'character-edit',
        meta: {title: 'PACT | character edit'},
    },
    {
        path: '/encounters',
        component: () => import('./components/Encounters.vue'),
        name: 'encounters',
        meta: {title: 'PACT | encounters'},
    },
    {
        path: '/encounters/:uuid',
        component: () => import('./components/Encounter.vue'),
        name: 'encounter',
        meta: {title: 'PACT | encounter'},
    },
    {
        path: '/encounters/create',
        component: () => import('./components/EncounterCreate.vue'),
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

// Modal stuff
Vue.use(VModal, { dynamic: true, injectModalsContainer: true })

// Autosize stuff
Vue.use(VueAutosize);

// Axios stuff
Vue.use(VueAxios, axios)

// Flash message stuff
Vue.use(FlashMessage);

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
