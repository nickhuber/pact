<template>
<div>
    <h4 class="title">Login</h4>
    <div class="notification is-danger" v-if="error">
        {{ error }}
    </div>
    <form @submit="handleSubmit">
        <div class="field">
            <label class="control" for="username">Username</label>
            <div class="control">
                <input class="input" id="username" type="text" v-model="username" required autofocus :class="{'is-danger': error}">
            </div>
        </div>
        <div class="field">
            <label class="control" for="password">Password</label>
            <div class="control">
                <input class="input" id="password" type="password" v-model="password" required :class="{'is-danger': error}">
            </div>
        </div>
        <div class="field">
            <div class="control">
                <button class="button is-link" type="submit">Login</button>
            </div>
        </div>
    </form>
</div>
</template>

<script>
export default {
    name: 'Login',
    data(){
        return {
            username : "",
            password : "",
            error: null,
        }
    },
    methods : {
        handleSubmit(e){
            e.preventDefault();
            this.$http.post(
                '/api/auth/login/   ',
                {
                    username: this.username,
                    password: this.password
                }
            ).then((response) => {
                if (response.status != 200) {
                    this.error = response.data;
                    return;
                }
                if (this.$route.params.nextUrl != null) {
                    this.$router.push(this.$route.params.nextUrl);
                } else {
                    this.$router.push({name: 'characters'});
                }
            }).catch(error => {
                this.error = error.response.data.error;
            });
        }
    }
}
</script>

<style>
</style>
