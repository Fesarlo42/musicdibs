<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Ajustes</h1>

    <div class="grid grid-cols-1 gap-7 md:grid-cols-5">
      <section class="order-1 pt-4 md:col-span-3 md:row-span-3">
        <UserData
          :userData="userData"
          :error="useUsersStore.error"
          @saveForm="updateUser"
          @deleteUser="handleDeleteUser"
        />
        <IdentityData
          v-if="userData && userData.role === 'user'"
          class="mt-7"
          :sigData="sigData"
          :error="useUsersStore.error"
        />
      </section>

      <section class="order-2 pt-4 md:col-span-2 md:row-span-2">
        <CreditHistory
          v-if="userData && userData.role === 'user'"
          :balance="creditsStore.balance"
          :transactionHistory="creditsStore.transactionHistory"
          :error="creditsStore.error"
        />
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

import { useUsersStore } from "../stores/users.js";
import { useAuthStore } from "../stores/auth.js";
import { useCreditsStore } from "../stores/credits.js";

import CreditHistory from "../components/CreditHistory.vue";
import UserData from "../components/UserData.vue";
import IdentityData from "../components/IdentityData.vue";

const creditsStore = useCreditsStore();
const authStore = useAuthStore();
const usersStore = useUsersStore();

const userData = ref({});
const sigData = ref({});

onMounted(async () => {
  userData.value = await usersStore.fetchUser(authStore.user.id);

  await creditsStore.fetchTransactionHistory(userData.value.id);
  await creditsStore.fetchBalance(userData.value.id);
  sigData.value = await usersStore.getSignatureInfo(userData.value.id);
});

const updateUser = async (form) => {
  await usersStore.updateUser(userData.value.id, form);
};

const handleDeleteUser = async () => {
  let confirm = window.confirm(
    "¿Estás seguro de que quieres eliminar tu cuenta? Esta acción no se puede deshacer.",
  );
  if (confirm) {
    await usersStore.deleteUser(userData.value.id);
    authStore.logout();
  }
};
</script>
