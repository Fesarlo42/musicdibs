<template>
  <div class="overflow-x-auto">
    <table class="table">
      <thead>
        <tr>
          <th class="hidden md:block">ID</th>
          <th class="w-1/4 md:whitespace-nowrap">Nombre</th>
          <th>Correo Electrónico</th>
          <th class="hidden md:block">Registrado el</th>
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
          <td class="hidden md:block">{{ user.id }}</td>
          <td class="w-1/4 capitalize md:whitespace-nowrap">
            {{ `${user.first_name} ${user.last_name}` }}
          </td>
          <td>{{ user.email }}</td>
          <td class="hidden md:block">{{ formatDate(user.created_at) }}</td>
          <td>
            <template v-if="userCredits[user.id] !== undefined">
              {{ userCredits[user.id] }}
            </template>
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
