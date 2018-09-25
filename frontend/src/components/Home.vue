<template>
  <div>
    <div class="login-page">
      <h1>Your Personal Todo List</h1>
      <form class="login-user" @submit.prevent="loginUser">
        <div class="login-label">
          <span> Username: </span>
          <input class="login-username" type="text" v-model="user.username" />
        </div>
        <div class="login-label">
          <span> Password: </span>
          <input class="login-password" type="password" v-model="user.password" />
        </div>
        <input class="login-submit" type="submit" value="Log In"/>
      </form>
      <h3>{{ errorMessage }}</h3>
      <form class="register-user" @submit="registerUser">
        <div class="login-label">
          <span class="register-label"> Username: </span>
          <input id="register-username" type="text"/>
        </div>
        <div class="login-label">
          <span class="register-label"> Password: </span>
          <input id="register-password" type="password"/>
        </div>
        <div class="login-label">
          <span class="register-label"> Repeat Password: </span>
          <input id="register-repeat-password" type="password"/>
        </div>
        <input class="login-register" type="submit" value="Register" />
      </form>
      <h2 id="register-error-message"></h2>
    </div>
  </div>
</template>
<style lang="scss">
@import "../assets/scss/_dashboard.scss";
</style>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      user: {
        username: '',
        password: ''
      },
      errorMessage: ''
    }
  },
  methods: {
    loginUser () {
      axios.post(this.$hostname + 'accounts/login/', {
        credentials: {
          username: this.user.username,
          password: this.user.password
        }
      })
        .then(response => {
          console.log(response)
          localStorage.name = response.data.data.token
          this.$router.push('Dashboard')
        })
        .catch(error => {
          console.log(error.response)
          this.errorMessage = error.response.data.message.description
        })
    },
    registerUser () {
      var registerPassword = document.getElementById('register-password').value
      var registerPasswordRepeat = document.getElementById('register-repeat-password').value
      if (registerPassword === registerPasswordRepeat) {
        axios.post(this.$hostname + 'accounts/register/', {
          credentials: {
            username: document.getElementById('register-username').value,
            password: registerPassword
          }
        })
          .then(response => {
            console.log(response)
          })
          .catch(error => {
            console.log(error.response)
            this.errorMessage = error.response.data.message.description
          })
      } else {
        alert('Password does not match')
      }
    }
  }
}

</script>
