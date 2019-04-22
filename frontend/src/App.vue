<template>
<div id="app" class="section">
    <div class="container">
        <div class="navbar">
            <div class="navbar-brand">
                <div class="navbar-item">
                    PACT
                </div>
            </div>
            <div class="navbar-item">
                <router-link :to="{name: 'characters'}">
                    Characters
                </router-link>
            </div>
            <div class="navbar-item">
                <router-link :to="{name: 'encounters'}">
                    Encounters
                </router-link>
            </div>
        </div>
        <div class="section">
            <div class="container">
                <div class="box">
                    <router-view></router-view>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
</script>

<style>
</style>
