<template>
<tr>
    <td>
        <span v-if="!character.is_player">
            <span @click="showDescription">
                <a href="javascript://">{{ character.name }}</a>
            </span>
        </span>
        <span v-if="character.is_player">
            {{ character.name }}
        </span>
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
        <input class="input" type="number" v-model.number="initiative" :disabled="formsDisabled">
    </td>
    <td>
        <button class="button is-primary" @click="add" :disabled="formsDisabled">Add</button>
        <button class="button is-danger" @click="remove" :disabled="formsDisabled">Remove</button>
    </td>
</tr>
</template>

<script>
import Modal from './Modal.vue';

export default {
    name: 'EncounterStagedCharacterRow',
    props: ['character', 'formsDisabled'],
    data() {
        return {
            initiative: null,
            notesEditing: false,
            newNotes: '',
        }
    },
    methods: {
        add() {
            this.$http.patch(
                `/api/encounter_characters/${this.character.uuid}`,
                {
                    initiative: this.initiative
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

<style scoped>
</style>
