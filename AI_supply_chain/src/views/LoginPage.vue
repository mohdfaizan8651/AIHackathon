<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" type="text" placeholder="Username" required />
      <select v-model="role">
        <option disabled value="">Select Role</option>
        <option>Planning</option>
        <option>Finance</option>
        <option>Admin</option>
      </select>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      role: ''
    };
  },
  methods: {
    login() {
      localStorage.setItem('username', this.username);
      localStorage.setItem('role', this.role);
      this.$router.push('/chat');
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 30px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  text-align: center;
  border-radius: 10px;
  background: #f9f9f9;
}
input, select, button {
  display: block;
  width: 100%;
  padding: 10px;
  margin-top: 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
}
button {
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #33996a;
}
</style>
