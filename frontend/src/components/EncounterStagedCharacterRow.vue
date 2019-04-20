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
            {{ character.notes }}
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
        }
    }
}
</script>

<style scoped>
</style>
