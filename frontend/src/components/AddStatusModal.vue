<template>
    <div class="section">
        <h1 class="title">Add status effect</h1>
        <form @submit="addStatusEffect">
            <div class="field">
                <label class="field-label is-normal" for="name">Name</label>
                <div class="field-body">
                    <input class="input" id="name" type="text" v-model="name" :class=" {'is-danger': errors.name}">
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
                    <input class="input" id="remaining_duration" type="number" v-model.number="remaining_duration" :class=" {'is-danger': errors.remaining_duration}">
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
                    <button class="button is-link" type="submit">Add</button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    export default {
        name: 'AddStatusModal',
        props: ['encounterCharacter'],
        data() {
            return {
                'name': '',
                'remaining_duration': 0,
                'errors': {},
            }
        },
        methods: {
        addStatusEffect() {
            let vm = this;
            let postData = {
                'character': vm.encounterCharacter.url,
                'name': vm.name,
                'remaining_duration': vm.remaining_duration,
            }
            this.$http.post(
                '/api/status_effects/',
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
