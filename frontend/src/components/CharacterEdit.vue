<template>
    <div id="character-edit">
        <div class="loading" v-if="loading">
            Loading...
        </div>
        <div v-if="character">
                <button class="button is-outlined is-primary" @click="handleSave">
                    <span>
                        Save
                    <font-awesome-icon icon="save"></font-awesome-icon>
                    </span>
                </button>
            <form>
                <div class="field">
                    <label class="field-label is-normal" for="name">Name</label>
                    <div class="field-body">
                        <input class="input" id="name" type="text" v-model="character.name" required :class="{'is-danger': errors.name}">
                    </div>
                    <p
                        class="help is-danger"
                        v-for="error in errors.name"
                        :key="error"
                    >
                        {{ error }}
                    </p>
                </div>
                <div v-if="!character.is_player">
                    <div class="field">
                        <label class="field-label is-normal" for="hit_dice">Hit dice</label>
                        <div class="field-body">
                            <input class="input" id="hit_dice" type="text" v-model="character.hit_dice" required :class="{'is-danger': errors.hit_dice}">
                        </div>
                        <p
                            class="help is-danger"
                            v-for="error in errors.hit_dice"
                            :key="error"
                        >
                            {{ error }}
                        </p>
                    </div>
                </div>
                <div class="field">
                    <label class="field-label is-normal" for="description">Description</label>
                    <div class="field-body">
                        <textarea class="textarea" id="description" v-model="character.description":class="{'is-danger': errors.description}"></textarea>
                    </div>
                    <p
                        class="help is-danger"
                        v-for="error in errors.description"
                        :key="error"
                    >
                        {{ error }}
                    </p>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import Character from './Character.vue';

export default {
    name: 'CharacterEdit',
    extends: Character,
    data() {
        return {
            errors: {},
        }
    },
    methods : {
        handleSave(e) {
            let vm = this;
            e.preventDefault();
            this.$http.patch(
                '/api/characters/' + vm.$route.params.uuid,
                this.character
            ).then((response) => {
                if (response.status != 200) {
                    vm.errors = response.data;
                    return;
                }
                vm.$router.push({name: 'character', params: {uuid: vm.character.uuid}});
            }).catch((error) => {
                vm.errors = error.response.data;
            });
        }
    }
}
</script>

<style scoped>
</style>
