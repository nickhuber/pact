<template>
<div id="character">
    <div class="loading" v-if="loading">
        Loading...
    </div>
    <div v-if="character" class="content">
        <p class="title">{{ character.name }}</p>
        <p class="subtitle">
            <span v-if="character.is_player">Player</span>
            <span v-if="!character.is_player">Non-player</span>
            character
        </p>
        <div class="navbar">
            <div class="navbar-item">
                <router-link class="button is-outlined is-link" :to="{name: 'character-edit', params: {uuid: character.uuid}}">
                    <span>
                        Edit
                        <font-awesome-icon icon="edit"></font-awesome-icon>
                    </span>
                </router-link>
            </div>
            <div class="navbar-item">
                <button class="button is-outlined is-danger" @click="handleDelete">
                    <span>
                        Delete
                        <font-awesome-icon icon="times"></font-awesome-icon>
                    </span>
                </button>
            </div>
        </div>
        <dl>
            <dt v-if="!character.is_player">Hit Dice</dt>
            <dd v-if="!character.is_player">{{ character.hit_dice }}</dd>

            <dt>Description</dt>
            <dd><vue-markdown>{{ character.description }}</vue-markdown></dd>
        </dl>
    </div>
</div>
</template>

<script>
import VueMarkdown from 'vue-markdown';

export default {
    name: 'Character',
    components: { VueMarkdown },
    data() {
        return {
            character: null,
            error: null,
            delete_error: null,
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
            this.error = this.character = null;
            this.loading = true;
            this.$http.get(`/api/characters/${vm.$route.params.uuid}`).then((response) => {
                vm.loading = false;
                vm.character = response.data;
            });
        },
        handleDelete() {
            let vm = this;
            this.$http.delete(`/api/characters/${vm.$route.params.uuid}`).then((response) => {
                if (response.status != 204) {
                    vm.delete_error = response.data;
                    return;
                }
                vm.$router.push({name: 'characters'});
            });
        }
    }
}
</script>

<style scoped>
</style>
