<template>
<section class="section">
    <vue-markdown>{{ text }}</vue-markdown>
</section>
</template>

<script>
const VueMarkdown = () => import('vue-markdown');
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
