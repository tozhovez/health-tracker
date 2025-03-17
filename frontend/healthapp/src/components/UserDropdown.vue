<template>
    <div>
      <label for="user-select">Выберите пользователя:</label>
      <select id="user-select" v-model="selectedUserUuid">
        <option v-for="user in users" :key="user.user_uuid" :value="user.user_uuid">
          {{ user.first_name }} {{ user.last_name }}
        </option>
      </select>
  
      <div v-if="selectedUser">
        <h3>Данные пользователя:</h3>
        <p><strong>Email:</strong> {{ selectedUser.email }}</p>
        <p><strong>Телефон:</strong> {{ selectedUser.phone_number }}</p>
        <p><strong>Адрес:</strong> {{ selectedUser.address }}</p>
        <p><strong>Дата рождения:</strong> {{ selectedUser.birthday }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import { fetchUsers } from "../services/UserService.js";
  
  export default {
    data() {
      return {
        users: [],
        selectedUserUuid: null,
      };
    },
    computed: {
      selectedUser() {
        return this.users.find(user => user.user_uuid === this.selectedUserUuid) || null;
      },
    },
    watch: {
      selectedUserUuid(newUuid) {
        this.$emit("user-selected", newUuid);
      },
    },
    async created() {
      this.users = await fetchUsers();
    },
  };
  </script>
  