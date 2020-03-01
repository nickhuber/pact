<template>
<section id="encounter">
    <div class="loading" v-if="!has_had_data">
        Loading...
    </div>
    <div v-if="encounter" class="content">  
        <p class="title">{{ encounter.name }}</p>
        <p class="subtitle">Encounter</p>

        <button class="button is-outlined is-danger" @click="deleteEncounter">
            <span>
                Delete
                <font-awesome-icon icon="times"></font-awesome-icon>
            </span>
        </button>

        <h2>Add character to encounter</h2>
        <section class="section">
            <EncounterAddCharacter
                :encounter="encounter"
                @encounter-character-added="onEncounterCharacterAdded"
            ></EncounterAddCharacter>
        </section>

        <div v-if="stagedCharacters.length > 0">
            <h2>Staged characters</h2>
            <section class="section">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Notes</th>
                            <th>Initiative</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <EncounterStagedCharacterRow
                            v-for="character in stagedCharacters"
                            :key="character.uuid"
                            :character="character"
                            :formsDisabled="formsDisabled"
                            @encounter-character-updated="onEncounterCharacterUpdated"
                        >
                        </EncounterStagedCharacterRow>
                    </tbody>
                </table>
            </section>
        </div>

        <div v-if="encounterCharacters.length > 0">
            <h2>The actual encounter</h2>
            <section class="section">
                <div>
                    <button @click="advanceInit" class="button is-small">Advance initiative</button>
                    round {{ encounter.current_round }}
                    <span v-if="encounter.current_initiative !== null">| initiative {{ encounter.current_initiative }}</span>
                </div>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Notes</th>
                            <th>Initiative</th>
                            <th>HP</th>
                            <th>Status effects</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <EncounterCharacterRow
                            :class="{'is-active-character': isActiveCharacter(character)}"
                            v-for="character in encounterCharacters"
                            :key="character.uuid"
                            :character="character"
                            :formsDisabled="formsDisabled"
                            @encounter-character-updated="onEncounterCharacterUpdated"
                        ></EncounterCharacterRow>
                    </tbody>
                </table>
            </section>
        </div>
    </div>
</section>
</template>

<script>
import EncounterAddCharacter from './EncounterAddCharacter.vue';
import EncounterCharacterRow from './EncounterCharacterRow.vue';
import EncounterStagedCharacterRow from './EncounterStagedCharacterRow.vue';

export default {
    name: 'Encounter',
    components: { EncounterAddCharacter, EncounterCharacterRow, EncounterStagedCharacterRow },
    data() {
        return {
            encounter: null,
            error: null,
            loading: false,
            has_had_data: false,
        }
    },
    created () {
        this.fetchData()
    },
    watch: {
        '$route': 'fetchData'
    },
    computed: {
        stagedCharacters: function() {
            function compare(a, b) {
                if (a.name > b.name) {
                    return -1;
                }
                if (a.name < b.name) {
                    return 1;
                }
                return 0;
            }
            if (this.encounter) {
                return [...this.encounter.characters].sort(compare).filter((character) => {
                    return character.initiative === null;
                });
            } else {
                return [];
            }
        },
        encounterCharacters: function() {
            function compare(a, b) {
                if (a.initiative > b.initiative) {
                    return -1;
                }
                if (a.initiative < b.initiative) {
                    return 1;
                }
                return 0;
            }
            if (this.encounter) {
                return [...this.encounter.characters].sort(compare).filter((character) => {
                    return character.initiative !== null;
                });
            } else {
                return [];
            }
        },
        formsDisabled : function () {
            return this.loading
        }
    },
    methods: {
        fetchData() {
            let vm = this;
            this.error;
            this.loading = true;
            this.$http.get(`/api/encounters/${vm.$route.params.uuid}`).then((response) => {
                vm.loading = false;
                vm.has_had_data = true;
                vm.encounter = response.data;
            });
        },
        deleteEncounter() {
            let vm = this;
            this.$http.delete(`/api/encounters/${vm.$route.params.uuid}`).then((response) => {
                vm.$router.push({name: 'encounters'});
            });
        },
        advanceInit() {
            let vm = this;
            this.$http.post(`/api/encounters/${vm.$route.params.uuid}/advance_initiative`).then((response) => {
                vm.encounter = response.data;
            });
        },
        isActiveCharacter(character) {
            return this.encounter.active_character_uuids.find((uuid) => {
                return character.uuid == uuid;
            });
        },
        onEncounterCharacterAdded() {
            this.fetchData();
        },
        onEncounterCharacterUpdated() {
            this.fetchData();
        }
    }
}
</script>

<style scoped>
tr.is-active-character {
    background-color: lightblue;
}
</style>
