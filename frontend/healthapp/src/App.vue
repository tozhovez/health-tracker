<template>
  <div>
    <h1>Выбор пользователя</h1>
    <UserDropdown @user-selected="handleUserSelection" />
    </div>
    <div>
    <PhysicalActivityChart v-if="selectedUserUuid" :userUuid="selectedUserUuid" />
  </div>

</template>

<script lang="ts">
import UserDropdown from "./components/UserDropdown.vue";
import PhysicalActivityChart from "./components/PhysicalActivityChart.vue";



export default {
  components: {
    UserDropdown,
    PhysicalActivityChart,
  },
  data() {
    return {
      selectedUserUuid: null,
    };
  },
  methods: {
    handleUserSelection(userUuid) {
      this.selectedUserUuid = userUuid;
    },
  },
};
</script>


