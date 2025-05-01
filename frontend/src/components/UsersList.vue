<template>
  <div class="w-full overflow-x-auto">
    <table class="table w-full">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Correo Electrónico</th>
          <th>Registrado El</th>
          <th>Créditos</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="user in users"
          :key="user.id"
          class="hover cursor-pointer"
          @click="navigateToUserDetail(user.id)"
        >
          <td>{{ user.id }}</td>
          <td class="capitalize">
            {{ `${user.first_name} ${user.last_name}` }}
          </td>
          <td>{{ user.email }}</td>
          <td>{{ formatDate(user.created_at) }}</td>
          <td>
            <div v-if="userCredits[user.id] !== undefined">
              {{ userCredits[user.id] }}
            </div>
            <div v-else class="flex items-center">
              <span class="loading loading-spinner loading-xs mr-2"></span>
            </div>
          </td>
        </tr>

        <tr v-if="users.length === 0">
          <td colspan="5" class="py-4 text-center">
            No hay usuarios para mostrar
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useCreditsStore } from "../stores/credits";
import { useRouter } from "vue-router";

const creditsStore = useCreditsStore();
const router = useRouter();

const props = defineProps({
  users: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const userCredits = ref({});

const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};

const loadUserCredits = async () => {
  for (const user of props.users) {
    try {
      const balance = await creditsStore.fetchBalance(user.id);
      userCredits.value[user.id] = balance;
    } catch (error) {
      console.error(`Error fetching credits for user ${user.id}:`, error);
      userCredits.value[user.id] = "Error";
    }
  }
};

watch(
  () => props.users,
  (newUsers) => {
    if (newUsers && newUsers.length > 0) {
      loadUserCredits();
    }
  },
  { immediate: true },
);

onMounted(() => {
  if (props.users && props.users.length > 0) {
    loadUserCredits();
  }
});

const navigateToUserDetail = (userId) => {
  router.push(`/manage_users/${userId}`);
};
</script>
