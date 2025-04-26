<template>
  <span
    v-if="authStore.isLoading"
    class="loading loading-spinner loading-xl"
  ></span>
</template>

<script setup>
import { onMounted } from "vue";
import { useAuthStore } from "../stores/auth.js";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

onMounted(() => {
  authStore.clearAuth();
  return router.push("/");
});
</script>
