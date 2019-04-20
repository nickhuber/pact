<template>
    <div class="section">
        <h1 class="title">Add status effect</h1>
        <form @submit="handleSave">
            <div class="field">
                <label class="field-label is-normal" for="name">Name</label>
                <div class="field-body">
                    <input class="input" id="name" type="text" v-model="statusEffect.name" :class=" {'is-danger': errors.name}">
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
                <label class="field-label is-normal" for="remaining_duration">duration</label>
                <div class="field-body">
                    <input class="input" id="remaining_duration" type="number" v-model.number="statusEffect.remaining_duration" :class=" {'is-danger': errors.remaining_duration}">
                </div>
                <p
                    class="help is-danger"
                    v-for="error in errors.remaining_duration"
                    :key="error"
                >
                    {{ error }}
                </p>
            </div>
            <div class="field">
                <div class="control">
                    <button class="button is-link" type="submit">Save</button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    export default {
        name: 'ChangeStatusModal',
        props: ['statusEffect'],
        data() {
            return {
                'errors': {},
            }
        },
        methods: {
        handleSave() {
            let vm = this;
            let postData = {
                'character': vm.statusEffect.character.url,
                'name': vm.statusEffect.name,
                'remaining_duration': vm.statusEffect.remaining_duration,
            }
            this.$http.patch(
                `/api/status_effects/${vm.statusEffect.uuid}`,
                postData
            ).then((response) => {
                vm.errors = {};
                this.$emit('status-effect-added');
                this.$emit('close');
            }).catch((error) => {
                vm.errors = error.response.data;
            });
        }
        },
    }
</script>

<style>
</style>
