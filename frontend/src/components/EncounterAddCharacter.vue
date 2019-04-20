<template>
    <div id="encounter-add-character">
        <form @submit="addCharacter">
            <div class="field">
                <div class="control">
                    <button class="button is-outlined is-primary">
                        <span>
                            Add to encounter
                        <font-awesome-icon icon="plus-square"></font-awesome-icon>
                        </span>
                    </button>
                </div>
            </div>
            <div class="field">
                <label class="field-label is-normal" for="character">Character</label>
                <div class="field-body">
                    <div class="select" :class="{'is-danger': errors.initiative}">
                        <select v-model="selectedCharacter">
                        <option disabled value="">-- Player Characters --</option>
                        <option v-for="character in players" :value="character.url" :key="character.uuid">
                            {{ character.name }}
                        </option>
                        <option disabled value="">-- Non-Player Characters --</option>
                        <option v-for="character in npcs" :value="character.url" :key="character.uuid">
                            {{ character.name }}
                        </option>
                        </select>
                    </div>
                </div>
                <p
                    class="help is-danger"
                    v-for="error in errors.character"
                    :key="error"
                >
                    {{ error }}
                </p>
            </div>
            <div class="field">
                <label class="field-label is-normal" for="initiative">Initiative</label>
                <div class="field-body">
                    <input class="input" id="initiative" type="number" v-model.number="initiative" :class=" {'is-danger': errors.initiative}">
                </div>
                <p
                    class="help is-danger"
                    v-for="error in errors.initiative"
                    :key="error"
                >
                    {{ error }}
                </p>
            </div>
            <div class="field">
                <label class="field-label is-normal" for="notes">Notes</label>
                <div class="field-body">
                    <input class="input" id="notes" type="text" v-model="notes" :class=" {'is-danger': errors.notes}">
                </div>
                <p
                    class="help is-danger"
                    v-for="error in errors.notes"
                    :key="error"
                >
                    {{ error }}
                </p>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    name: 'EncounterAddCharacter',
    props: ['encounter'],
    data() {
        return {
            characters: [],
            players: [],
            npcs: [],
            selectedCharacter: null,
            initiative: null,
            notes: '',
            errors: {},
        }
    },
    created () {
        this.fetchData()
    },
    methods : {
        fetchData() {
            function sortByName(a, b) {
                if (a.name.toLowerCase() < b.name.toLowerCase()) {
                    return -1;
                }
                if (a.name.toLowerCase() > b.name.toLowerCase()) {
                    return 1;
                }
                return 0;
            }
            let vm = this;
            this.characters = null;
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
                vm.players.sort(sortByName);
                vm.npcs.sort(sortByName);
                vm.loading = false;
            });
        },
        addCharacter() {
            let vm = this;
            let postData = {
                'encounter': vm.encounter.url,
                'character': vm.selectedCharacter,
                'initiative': vm.initiative == '' ? null : vm.initiative,
                'notes': vm.notes,
            }
            this.$http.post(
                '/api/encounter_characters/',
                postData
            ).then((response) => {
                vm.errors = {};
                vm.initiative = null;
                vm.notes = '';
                this.$emit('encounter-character-added');
            }).catch((error) => {
                vm.errors = error.response.data;
            });
        }
    }
}
</script>

<style scoped>
</style>
