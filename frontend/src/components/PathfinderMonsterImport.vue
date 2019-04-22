<template>
<section>
    <Autocomplete
        url="/api/pathfinder_monsters"
        param="name_search_term"
        anchor="title"
        label="writer"
        placeholder="Search for an existing template"
        debound="200"
        :on-select="getData"
        :onShouldRenderChild="renderChild"
        :classes="{ wrapper: 'control', input: 'input', list: 'list', item: 'is-active' }"
    >
    </Autocomplete>

</section>
</template>

<script>
import Autocomplete from 'vue2-autocomplete-js'

export default {
    name: "PathfinderMonsterImport",
    components: { Autocomplete },
    data() {
        return {
            metthod: 'name__icontains'
        };
    },
    methods: {
        getData(obj){
            this.$emit('pathfinder-monster-chosen', obj);
        },
        renderChild(data) {
            return `
                <span>${data.name} - CR ${data.cr}</span>
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
