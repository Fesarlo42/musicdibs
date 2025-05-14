<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Gestionar usuario</h1>

    <section
      v-if="
        useProjectsStore.error ||
        useUsersStore.error ||
        useAuthStore.error ||
        useCreditsStore.error
      "
    >
      <div
        v-if="useAuthStore.error"
        role="alert"
        class="alert alert-soft alert-error"
      >
        <span>{{ useAuthStore.error }}</span>
      </div>
      <div
        v-if="useCreditsStore.error"
        role="alert"
        class="alert alert-soft alert-error"
      >
        <span>{{ useCreditsStore.error }}</span>
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
      <div class="musicdibs-card bg-base-100">
        <div class="card-body">
          <h2 class="card-title">Detalles del usuario</h2>
          <div v-if="userData && userData.id" class="grid grid-cols-2 gap-8">
            <div>
              <p class="my-2">
                <span class="pr-2 font-semibold">Nombre:</span>
                <span class="capitalize">
                  {{ `${userData.first_name} ${userData.last_name}` }}
                </span>
              </p>
              <p class="my-2">
                <span class="pr-2 font-semibold">Correo electrónico:</span>
                <span>
                  {{ userData.email }}
                </span>
              </p>
              <p class="my-2">
                <span class="pr-2 font-semibold">Creditos:</span>
                <span>
                  {{ userBalance }}
                </span>
              </p>
            </div>

            <div class="flex flex-col gap-2">
              <button
                class="btn btn-primary btn-link btn-sm w-auto self-start border-0"
                @click="handleModal"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  class="size-6"
                >
                  <path
                    d="M12 7.5a2.25 2.25 0 1 0 0 4.5 2.25 2.25 0 0 0 0-4.5Z"
                  />
                  <path
                    fill-rule="evenodd"
                    d="M1.5 4.875C1.5 3.839 2.34 3 3.375 3h17.25c1.035 0 1.875.84 1.875 1.875v9.75c0 1.036-.84 1.875-1.875 1.875H3.375A1.875 1.875 0 0 1 1.5 14.625v-9.75ZM8.25 9.75a3.75 3.75 0 1 1 7.5 0 3.75 3.75 0 0 1-7.5 0ZM18.75 9a.75.75 0 0 0-.75.75v.008c0 .414.336.75.75.75h.008a.75.75 0 0 0 .75-.75V9.75a.75.75 0 0 0-.75-.75h-.008ZM4.5 9.75A.75.75 0 0 1 5.25 9h.008a.75.75 0 0 1 .75.75v.008a.75.75 0 0 1-.75.75H5.25a.75.75 0 0 1-.75-.75V9.75Z"
                    clip-rule="evenodd"
                  />
                  <path
                    d="M2.25 18a.75.75 0 0 0 0 1.5c5.4 0 10.63.722 15.6 2.075 1.19.324 2.4-.558 2.4-1.82V18.75a.75.75 0 0 0-.75-.75H2.25Z"
                  />
                </svg>
                Gestionar creditos
              </button>
              <button
                class="btn btn-primary btn-link btn-sm w-auto self-start border-0"
                @click="handleDeleteUser"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  class="size-6"
                >
                  <path
                    fill-rule="evenodd"
                    d="M16.5 4.478v.227a48.816 48.816 0 0 1 3.878.512.75.75 0 1 1-.256 1.478l-.209-.035-1.005 13.07a3 3 0 0 1-2.991 2.77H8.084a3 3 0 0 1-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 0 1-.256-1.478A48.567 48.567 0 0 1 7.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 0 1 3.369 0c1.603.051 2.815 1.387 2.815 2.951Zm-6.136-1.452a51.196 51.196 0 0 1 3.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 0 0-6 0v-.113c0-.794.609-1.428 1.364-1.452Zm-.355 5.945a.75.75 0 1 0-1.5.058l.347 9a.75.75 0 1 0 1.499-.058l-.346-9Zm5.48.058a.75.75 0 1 0-1.498-.058l-.347 9a.75.75 0 0 0 1.5.058l.345-9Z"
                    clip-rule="evenodd"
                  />
                </svg>
                Borrar usuario
              </button>
            </div>
          </div>
          <section v-else>
            <div class="loading loading-spinner text-primary"></div>
          </section>
        </div>
      </div>
    </section>
  </div>

  <CreditsModal
    v-if="userData && userData.id && userBalance"
    :userId="userData.id"
    :balance="userBalance"
    @balance-updated="() => creditsStore.fetchBalance(userData.id)"
  />
</template>

<script setup>
import { onMounted, computed, ref } from "vue";
import { useRouter, useRoute } from "vue-router";

import { useProjectsStore } from "../stores/projects.js";
import { useUsersStore } from "../stores/users.js";
import { useCreditsStore } from "../stores/credits.js";
import { useAuthStore } from "../stores/auth.js";

import CreditsModal from "../components/CreditsModal.vue";

const projectsStore = useProjectsStore();
const creditsStore = useCreditsStore();
const usersStore = useUsersStore();
const authStore = useAuthStore();

const route = useRoute();
const router = useRouter();

const userData = ref(null);
const userProjects = ref([]);

const userBalance = computed(() => {
  return creditsStore.balance;
});

onMounted(async () => {
  const isAllowed = await authStore.checkPermission("admin");

  if (!isAllowed) {
    return router.push("/unauthorized");
  }

  const ref = route.params.ref;
  if (ref) {
    userData.value = await usersStore.fetchUser(ref);
    userProjects.value = await projectsStore.fetchProjects({ user_id: ref });
    await creditsStore.fetchBalance(ref);
  } else {
    console.error("Missing user ref in route params");
  }
});

const handleDeleteUser = async () => {
  let confirm = window.confirm(
    "¿Estás seguro de que quieres eliminar ese usuario? Esta acción no se puede deshacer.",
  );
  if (confirm) {
    await usersStore.deleteUser(userData.value.id);
    router.push("/dashboard_admin");
  }
};

const handleModal = () => {
  const modal = document.getElementById("credits_modal");
  credits_modal.showModal();
};
</script>
