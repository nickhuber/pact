<template>
    <div id="encounter-create">
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
                <label class="field-label is-normal" for="name">Name</label>
                <div class="field-body">
                    <input class="input" id="name" type="text" v-model="encounter.name" required :class=" {'is-danger': errors.name}">
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
                <label class="field-label is-normal" for="hit_dice">notes</label>
                <div class="field-body">
                    <textarea class="textarea" id="notes" v-model="encounter.notes" :class=" {'is-danger': errors.notes}"></textarea>
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
    name: 'EncounterCreate',
    data() {
        return {
            encounter: {
                uuid: null,
                name: '',
                notes: '',
            },
            errors: {},
        }
    },
    methods : {
        handleSave(e) {
            e.preventDefault();
            let vm = this;
            let postData = {
                name: this.encounter.name,
                notes: this.encounter.notes,
            };
            this.$http.post(
                '/api/encounters/',
                postData
            ).then((response) => {
                vm.encounter = response.data;
                vm.$router.push({name: 'encounter', params: {uuid: vm.encounter.uuid}});
            }).catch((error) => {
                vm.errors = error.response.data;
            });
        }
    }
}
</script>

<style scoped>
</style>
