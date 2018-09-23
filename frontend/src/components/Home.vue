<template>
  <div>
    <div>
      <p>Home page</p>
      <form class="login-user" @submit.prevent="loginUser">
        <label>
          Username:
          <input type="text" v-model="user.username" />
        </label>
        <label>
          Password:
          <input type="text" v-model="user.password" />
        </label>
        <button type="submit">Submit</button>
      </form>
    </div>
    <div>
      <h3>{{ errorMessage }}</h3>
    </div>
    <about></about>
  </div>
</template>

<script>
import axios from 'axios'
import About from './About.vue'
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
  components: {
    About
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
    }
  }
}

</script>
