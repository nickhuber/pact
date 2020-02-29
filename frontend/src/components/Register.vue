<template>
<div>
    <h4 class="title">Register</h4>
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
            <label class="control" for="username">Email</label>
            <div class="control">
                <input class="input" id="email" type="text" v-model="email" required autofocus :class="{'is-danger': error}">
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
                <button class="button is-link" type="submit">Sign up</button>
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
            email : "",
            password : "",
            error: null,
        }
    },
    methods : {
        handleSubmit(e){
            e.preventDefault();
            this.$http.post(
                '/api/auth/register/',
                {
                    username: this.username,
                    email: this.email,
                    password: this.password
                }
            ).then((response) => {
                if (response.status != 200) {
                    this.error = response.data;
                    return;
                }
                this.$router.push({name: 'login'});
            }).catch(error => {
                this.error = error.response.data.error;
            });
        }
    }
}
</script>

<style>
</style>
