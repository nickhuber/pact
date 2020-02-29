<template>
<div>
    <p>
    PACT is a combat tracker for tabletop gaming. It is designed to just
    manage combat encounters in a simple fashion, while leaving most of the work
    still on the physical tabletop. It can track initiative, status effects, hit
    points and whatever extra information you want to make eaily available for a
    character. Feel free to <router-link :to="{name: 'register'}">register</router-link>
    or <router-link :to="{name: 'login'}">login</router-link> and start using it.
    </p>
    <p>
    This is a work in progress and new features will be added periodically. You can
    email <a href="mailto:pact@nickhuber.ca">pact@nickhuber.ca</a> With any feature
    requests or bug reports.
    </p>
</div>
</template>

<script>
export default {
    name: 'Overview',
}
</script>

<style>
</style>
