<template>
<tr>
    <td>
        <div class="vertical-center">
            <span v-if="!character.is_player">
                <span @click="showDescription">
                    <a href="javascript://">{{ character.name }}</a>
                </span>
            </span>
            <span v-if="character.is_player">
                {{ character.name }}
            </span>
        </div>
    </td>
    <td>
        <div class="vertical-center">
            <div v-if="!notesEditing">
                <div class="level">
                    <div class="level-item">
                        <span>{{ character.notes }}</span>
                    </div>
                    <div class="level-item">
                        <button class="button is-small" @click="enableEditing">Edit</button>
                    </div>
                </div>
            </div>
            <div v-if="notesEditing" class="level">
                <div class="level-item">
                    <input v-model="newNotes" class="input is-small"/>
                </div>
                <div class="level-item">
                    <button class="button is-small" @click="disableEditing">Cancel</button>
                </div>
                <div class="level-item">
                    <button class="button is-small" @click="saveEdit">Save</button>
                </div>
            </div>
        </div>
    </td>
    <td>
        <div class="vertical-center">
            <div class="level">
                <div class="level-item">
                    {{ character.initiative }}
                </div>
                <div class="level-item">
                    <button class="button is-small" @click="increaseInitiative" :disabled="formsDisabled"><font-awesome-icon icon="arrow-up"></font-awesome-icon></button>
                    <button class="button is-small" @click="decreaseInitiative" :disabled="formsDisabled"><font-awesome-icon icon="arrow-down"></font-awesome-icon></button>
                </div>
            </div>
        </div>
    </td>
    <td>
        <div v-if="!character.is_player" class="vertical-center">
            <div class="columns">
                <div class="column is-one-fifth">
                    <div class="fraction">
                        <span class="fraction-numerator">
                            {{ character.current_hp }}
                        </span>
                        <span class="fraction-bar">
                            /
                        </span>
                        <span class="fraction-denominator">
                            {{ character.max_hp }}
                        </span>
                    </div>
                </div>
                <div class="column">
                    <div class="level">
                        <div class="level-item">
                            <button class="button is-small is-fullwidth is-warning" @click="hurt" :disabled="formsDisabled">Hurt</button>
                        </div>
                        <div class="level-item is-two-fifths">
                            <input class="input is-small" type="number" v-model.number="hp_change_value" :disabled="formsDisabled">
                        </div>
                        <div class="level-item">
                            <button class="button is-small is-fullwidth is-success" @click="heal" :disabled="formsDisabled">Heal</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </td>
    <td>
        <div v-if="character.status_effects.length > 0" class="vertical-center">
            <ul class="status-list">
                <li v-for="status in character.status_effects" :key="status.url">
                    <span>
                        <a @click="changeStatusEffect(status)">{{ status.name }}</a> - {{ status.remaining_duration }} turn<span v-if="status.remaining_duration > 1">s</span>
                    </span>
                    <a class="is-pulled-right" @click="removeStatusEffect(status)">
                        <font-awesome-icon icon="times"></font-awesome-icon>
                    </a>
                </li>

            </ul>
        </div>
    </td>
    <td>
        <div class="vertical-center">
            <button class="is-vcentered button is-small is-danger" @click="remove" :disabled="formsDisabled">Remove</button>
            <button class="is-vcentered button is-small is-info" @click="addStatusEffect" :disabled="formsDisabled">Add status effect</button>
        </div>
    </td>
</tr>
</template>

<script>
const Modal = () => import('./Modal.vue');
const AddStatusModal = () => import('./AddStatusModal.vue');
const ChangeStatusModal = () => import('./ChangeStatusModal.vue');

export default {
    name: 'EncounterCharacterRow',
    props: ['character', 'formsDisabled'],
    data() {
        return {
            hp_change_value: null,
            notesEditing: false,
            newNotes: '',
        }
    },
    methods: {
        hurt() {
            if (this.hp_change_value == null || this.hp_change_value == '') {
                return;
            }
            this.$http.patch(
                `/api/encounter_characters/${this.character.uuid}`,
                {
                    current_hp: this.character.current_hp - this.hp_change_value
                }
            ).then((response) => {
                this.character.current_hp = response.data.current_hp;
                this.$emit('encounter-character-updated');
                this.hp_change_value = null;
            });
        },
        heal() {
            if (this.hp_change_value == null || this.hp_change_value == '') {
                return;
            }
            this.$http.patch(
                `/api/encounter_characters/${this.character.uuid}`,
                {
                    current_hp: this.character.current_hp + this.hp_change_value
                }
            ).then((response) => {
                this.character.current_hp = response.data.current_hp;
                this.$emit('encounter-character-updated');
                this.hp_change_value = null;
            });
        },
        increaseInitiative() {
            this.$http.patch(
                `/api/encounter_characters/${this.character.uuid}`,
                {
                    initiative: this.character.initiative + 1
                }
            ).then((response) => {
                this.character.initiative = response.data.initiative;
                this.$emit('encounter-character-updated');
            });
        },
        decreaseInitiative() {
            this.$http.patch(
                `/api/encounter_characters/${this.character.uuid}`,
                {
                    initiative: this.character.initiative - 1
                }
            ).then((response) => {
                this.character.initiative = response.data.initiative;
                this.$emit('encounter-character-updated');
            });
        },
        remove() {
            this.$http.delete(
                `/api/encounter_characters/${this.character.uuid}`
            ).then((response) => {
                this.$emit('encounter-character-updated');
            });
        },
        showDescription() {
            this.$modal.show(Modal, {
                text: this.character.description,
            }, {
                width: "80%",
                height: "80%",
            });
        },
        addStatusEffect() {
            this.$modal.show(AddStatusModal, {
                encounterCharacter: this.character,
            }, {
                width: "80%",
                height: "80%",
            }, {
                // This might not be the perfect way of doing this, but it keeps the encounter in sync
                'closed': (event) => { this.$emit('encounter-character-updated'); }
            });
        },
        changeStatusEffect(status) {
            this.$modal.show(ChangeStatusModal, {
                statusEffect: status,
            }, {
                width: "80%",
                height: "80%",
            }, {
                // This might not be the perfect way of doing this, but it keeps the encounter in sync
                'closed': (event) => { this.$emit('encounter-character-updated'); }
            });
        },
        removeStatusEffect(status) {
            this.$http.delete(
                `/api/status_effects/${status.uuid}`
            ).then((response) => {
                this.$emit('encounter-character-updated');
            });
        },
        enableEditing: function(){
            this.newNotes = this.character.notes;
            this.notesEditing = true;
        },
        disableEditing: function(){
            this.newNotes = null;
            this.notesEditing = false;
        },
        saveEdit: function(){
            this.$http.patch(
                `/api/encounter_characters/${this.character.uuid}`,
                {
                    notes: this.newNotes
                }
            ).then((response) => {
                this.character.notes = response.data.notes;
                this.$emit('encounter-character-updated');
                this.hp_change_value = null;
            });
            this.disableEditing();
        }
    }
}
</script>

<style scoped lang="scss">
.columns {
    margin-bottom: 0px;
}
.fraction {
    display: inline-block;
    position: relative;
    vertical-align: middle;
    letter-spacing: 0.001em;
    text-align: center;
    font-size: 1em;
    > span {
        display: block;
    }
    span.fraction-denominator {
        border-top: thin solid;
    }
    span.fraction-bar {
        display: none;
    }
}

.status-list {
    margin: 0px;
    list-style: none;
    width: 100%;
}

// Vertical center the things in the table cells
td div {
    height: 100%;
    margin: 0;
    padding:0;
}
tr, td {
    height: 100%;
}

.vertical-center {
    display: flex;
    align-items: center;
    height: 100%;

}
</style>
