<template>
<div id="encounters">
    <h1 class="title">Encounters</h1>

    <div class="navbar">
        <div class="navbar-item">
            <router-link class="button is-outlined is-link" :to="{name: 'encounter-create'}">
                <span>
                    New
                    <font-awesome-icon icon="plus-square"></font-awesome-icon>
                </span>
            </router-link>
        </div>
    </div>

    <div class="loading" v-if="loading">
        Loading...
    </div>

    <div v-if="encounters">
        <ul>
            <li v-for="encounter in encounters" :key="encounter.uuid">
                <router-link :to="{name: 'encounter', params: {uuid: encounter.uuid}}">
                    {{ encounter.name }}
                </router-link>
            </li>
        </ul>
    </div>
</div>
</template>

<script>
export default {
    name: 'Encounters',
    data() {
        return {
            encounters: null,
            error: null,
            loading: false
        }
    },
    created () {
        this.fetchData()
    },
    watch: {
        '$route': 'fetchData'
    },
    methods: {
        fetchData() {
            let vm = this;
            this.error = this.encounters = null;
            this.loading = true;
            this.$http.get('/api/encounters/').then((response) => {
                vm.encounters = response.data;
                vm.loading = false;
            });
        }
    }
}
</script>

<style scoped>
</style>
