<template>
<section>
    <Autocomplete
        url="/api/5e_monsters"
        param="name_search_term"
        anchor="title"
        label="writer"
        placeholder="Search for a fifth edition template"
        :debounce="200"
        :on-select="getData"
        :onShouldRenderChild="renderChild"
        :classes="{ wrapper: 'control', input: 'input', list: 'list', item: 'is-active' }"
    >
    </Autocomplete>
</section>
</template>

<script>
import Autocomplete from 'vue2-autocomplete-js';

export default {
    name: "FifthEditionMonsterImport",
    components: { Autocomplete },
    data() {
        return {
            metthod: 'name__icontains'
        };
    },
    methods: {
        getData(obj){
            this.$emit('fifth-edition-monster-chosen', obj);
        },
        renderChild(data) {
            return `
                <span>${data.name} - ${data.cr}</span>
            `
        },
    }
};
</script>

<style scoped>
.autocomplete-list ul {
    margin-top: 0px;
    padding-top: 0px;
}
</style>
