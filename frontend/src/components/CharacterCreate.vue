<template>
    <div id="character-create">
        <div>
            <form @submit="handleSave">
                <div class="field">
                    <div class="control">
                        <button class="button is-outlined is-primary">
                            <span>
                                Create
                            <font-awesome-icon icon="plus-square"></font-awesome-icon>
                            </span>
                        </button>
                    </div>
                </div>
                <div class="field">
                    <label for="is_player" class="checkbox">
                        Player
                        <input type="checkbox" v-model="character.is_player" :class=" {'is-danger': errors.is_player}">
                    </label>
                    <p
                        class="help is-danger"
                        v-for="error in errors.is_player"
                        :key="error"
                    >
                        {{ error }}
                    </p>
                </div>
                <div class="field">
                    <label class="field-label is-normal" for="name">Name</label>
                    <div class="field-body">
                        <input class="input" id="name" type="text" v-model="character.name" required :class=" {'is-danger': errors.name}">
                    </div>
                    <p
                        class="help is-danger"
                        v-for="error in errors.name"
                        :key="error"
                    >
                        {{ error }}
                    </p>
                </div>
                <div class="field">
                    <label class="field-label is-normal" for="hit_dice">Hit dice</label>
                    <div class="field-body">
                        <input class="input" id="hit_dice" type="text" v-model="character.hit_dice" :disabled="character.is_player" :class=" {'is-danger': errors.hit_dice}">
                    </div>
                    <p
                        class="help is-danger"
                        v-for="error in errors.hit_dice"
                        :key="error"
                    >
                        {{ error }}
                    </p>
                </div>
                <div class="field">
                    <label class="field-label is-normal" for="description">Description</label>
                    <div class="field-body">
                        <textarea class="textarea" id="description" v-model="character.description" :class=" {'is-danger': errors.description}"></textarea>
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
export default {
    name: 'CharacterCreate',
    data() {
        return {
            character: {
                uuid: null,
                is_player: false,
                name: '',
                hit_dice: '',
                description: '',
            },
            errors: {},
        }
    },
    methods : {
        handleSave(e) {
            e.preventDefault();
            let vm = this;
            let postData = {
                name: this.character.name,
                is_player: this.character.is_player,
                description: this.character.description
            };
            if (!this.character.is_player) {
                postData.hit_dice = this.character.hit_dice;
            }
            this.$http.post(
                '/api/characters/',
                postData
            ).then((response) => {
                vm.errors = {}
                vm.character = response.data;
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
