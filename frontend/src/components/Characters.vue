<template>
<div id="characters">
    <h1 class="title">Characters</h1>

    <div class="navbar">
        <div class="navbar-item">
            <router-link class="button is-outlined is-link" :to="{name: 'character-create'}">
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

    <div v-if="characters">
        <h2 class="subtitle">Players</h2>
        <ul>
            <li v-for="player in players" :key="player.uuid">
                <router-link :to="{name: 'character', params: {uuid: player.uuid}}">{{ player.name }}</router-link>
            </li>
        </ul>

        <hr>

        <h2 class="subtitle">NPCs</h2>
        <ul>
            <li v-for="npc in npcs" :key="npc.uuid">
                <router-link :to="{name: 'character', params: {uuid: npc.uuid}}">{{ npc.name }}</router-link>
            </li>
        </ul>
    </div>
</div>
</template>

<script>
export default {
    name: 'Characters',
    data() {
        return {
            characters: null,
            players: null,
            npcs: null,
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
            this.error = this.characters = null;
            this.loading = true;
            this.$http.get('/api/characters/').then((response) => {
                vm.characters = response.data;
                vm.players = [];
                vm.npcs = [];
                vm.characters.forEach((character) => {
                    if (character.is_player) {
                        vm.players.push(character);
                    } else {
                        vm.npcs.push(character);
                    }
                })
                vm.loading = false;
            });
        }
    }
}
</script>

<style scoped>
</style>
