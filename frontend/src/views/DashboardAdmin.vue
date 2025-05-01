<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Dashboard de administración</h1>

    <section
      v-if="useProjectsStore.error || useUsersStore.error || useAuthStore.error"
    >
      <div
        v-if="useAuthStore.error"
        role="alert"
        class="alert alert-soft alert-error"
      >
        <span>{{ useAuthStore.error }}</span>
      </div>
      <div
        v-if="useProjectsStore.error"
        role="alert"
        class="alert alert-soft alert-error"
      >
        <span>{{ useProjectsStore.error }}</span>
      </div>
      <div
        v-if="useUsersStore.error"
        role="alert"
        class="alert alert-soft alert-error"
      >
        <span>{{ useUsersStore.error }}</span>
      </div>
    </section>

    <section class="pt-4">
      <SummaryAdmin
        :totalUsers="totalUsers"
        :totalProjectsCreated="totalProjectsCreated"
        :totalProjectsRegistered="totalProjectsRegistered"
      />
    </section>

    <section class="mt-10">
      <div class="musicdibs-card bg-base-100">
        <div class="card-body">
          <h2 class="card-title">Listado de usuarios</h2>
          <p>Pincha en el usuario para gestionarlo.</p>
          <UsersList :users="usersStore.users" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from "vue";
import { useRouter } from "vue-router";

import { useProjectsStore } from "../stores/projects.js";
import { useUsersStore } from "../stores/users.js";
import { useAuthStore } from "../stores/auth.js";

import SummaryAdmin from "../components/SummaryAdmin.vue";
import UsersList from "../components/UsersList.vue";

const projectsStore = useProjectsStore();
const usersStore = useUsersStore();
const authStore = useAuthStore();
const router = useRouter();

const projectStats = ref({});

const totalProjectsCreated = computed(() => {
  return projectStats.value.total_projects || 0;
});
const totalProjectsRegistered = computed(() => {
  return projectStats.value.total_registrations || 0;
});
const totalUsers = computed(() => {
  return usersStore.users.length || 0;
});

onMounted(async () => {
  const isAllowed = await authStore.checkPermission("admin");

  if (!isAllowed) {
    return router.push("/unauthorized");
  }

  projectStats.value = await projectsStore.fetchProjectsStats();

  await usersStore.fetchUsers();
});
</script>
