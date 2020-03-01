<template>
<section class="section">
    <vue-markdown>{{ text }}</vue-markdown>
</section>
</template>

<script>
import VueMarkdown from 'vue-markdown';

export default {
    name: 'Modal',
    props: ['text'],
    components: { VueMarkdown },
}
</script>

<style>
.section {
    overflow: auto;
    height: 100%;
}
</style>
