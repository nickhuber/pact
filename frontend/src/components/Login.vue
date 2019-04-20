<template>
    <div>
        <h4 class="title">Login</h4>
        <form @submit="handleSubmit">
            <div class="field">
                <label class="control" for="username">Username</label>
                <div class="control">
                    <input class="input" id="username" type="text" v-model="username" required autofocus>
                </div>
            </div>
            <div class="field">
                <label class="control" for="password">Password</label>
                <div class="control">
                    <input class="input" id="password" type="password" v-model="password" required>
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
                errors: null
            }
        },
        methods : {
            handleSubmit(e){
                e.preventDefault();
                this.$http.post(
                    '/api/auth/',
                    {
                        username: this.username,
                        password: this.password
                    }
                ).then((response) => {
                    if (response.status != 200) {
                        this.errors = response.data;
                        return;
                    }
                    if (this.$route.params.nextUrl != null) {
                        this.$router.push(this.$route.params.nextUrl);
                    } else {
                        this.$router.push({name: 'Characters'});
                    }
                }).catch(error => {
                    console.error(error.response);
                });
            }
        }
    }
</script>

<style>
</style>
