<template>
    <tr>
        <td>
            <span @click="showDescription">
                <a href="javascript://">{{ character.name }}</a>
            </span>
        </td>
        <td>
        </td>
        <td>
            <div class="level">
                <div class="level-item">
                    {{ character.initiative }}
                </div>
                <div class="level-item">
                    <button class="button is-small" @click="increaseInitiative" :disabled="formsDisabled"><font-awesome-icon icon="arrow-up"></font-awesome-icon></button>
                    <button class="button is-small" @click="decreaseInitiative" :disabled="formsDisabled"><font-awesome-icon icon="arrow-down"></font-awesome-icon></button>
                </div>
            </div>
        </td>
        <td>
            <span v-if="!character.is_player">
                <div class="level">
                    <div class="level-item">
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
                    <div class="level-item">
                        <button class="button is-fullwidth is-warning" @click="hurt()" :disabled="formsDisabled">Hurt</button>
                    </div>
                    <div class="level-item is-two-fifths">
                        <input class="input" type="number" v-model.number="hp_change_value" :disabled="formsDisabled">
                    </div>
                    <div class="level-item">
                        <button class="button is-fullwidth is-success" @click="heal()" :disabled="formsDisabled">Heal</button>
                    </div>
                </div>
            </span>
        </td>
        <td>
            <!-- TOOD: status effects -->
        </td>
        <td>
            <button class="button is-danger" @click="remove" :disabled="formsDisabled">Remove</button>
        </td>
    </tr>
</template>

<script>
import Modal from './Modal.vue';

export default {
    name: 'EncounterCharacterRow',
    props: ['character', 'formsDisabled'],
    data() {
        return {
            hp_change_value: null,
        }
    },
    methods: {
        hurt() {
            this.$http.patch(
                '/api/encounter_characters/' + this.character.uuid,
                {
                    current_hp: this.character.current_hp - this.hp_change_value
                }
            ).then((response) => { 
                this.character.current_hp = response.data.current_hp;
                this.$emit('encounter-character-updated');
            });
        },
        heal() {
            this.$http.patch(
                '/api/encounter_characters/' + this.character.uuid,
                {
                    current_hp: this.character.current_hp + this.hp_change_value
                }
            ).then((response) => { 
                this.character.current_hp = response.data.current_hp;
                this.$emit('encounter-character-updated');
            });
        },
        increaseInitiative() {
            this.$http.patch(
                '/api/encounter_characters/' + this.character.uuid,
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
                '/api/encounter_characters/' + this.character.uuid,
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
                '/api/encounter_characters/' + this.character.uuid
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

<style scoped lang="scss">
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
            border-top: thin solid  ;
    }
    span.fraction-bar {
            display: none;
    }
}
</style>
