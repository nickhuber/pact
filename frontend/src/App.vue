<template>
<div id="app" class="section">
    <FlashMessage :position="'right top'"/>
    <div class="container">
        <div class="navbar">
            <div class="navbar-brand">
                <div class="navbar-item">
                    <router-link :to="{name: 'overview'}">
                        PACT
                    </router-link>
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
            <div class="navbar-item">
                <a href="javascript://" @click="logout">
                    Logout
                </a>
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
export default {
    methods: {
        logout() {
            this.$http.post('/api/auth/logout').then(
                (response) => {
                    this.flashMessage.success({title: 'Logged out'});
                    this.$router.push({name: 'overview'});
                }
            )
        }
    }
}
</script>

<style lang="scss">
._vue-flash-msg-body {
    z-index: 1000;
}
</style>
