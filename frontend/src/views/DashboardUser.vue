<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Dashboard</h1>

    <section
      class="px-4"
      v-if="
        useProjectsStore.error || useCreditsStore.error || useAuthStore.error
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
        v-if="useProjectsStore.error"
        role="alert"
        class="alert alert-soft alert-error"
      >
        <span>{{ useProjectsStore.error }}</span>
      </div>
      <div
        v-if="useCreditsStore.error"
        role="alert"
        class="alert alert-soft alert-error"
      >
        <span>{{ useCreditsStore.error }}</span>
      </div>
    </section>

    <div class="grid grid-cols-1 gap-7 px-4 md:grid-cols-4">
      <section class="order-1 pt-4 md:col-span-4">
        <SummaryUser />
      </section>

      <section class="order-2 pt-4 md:col-span-2">
        <div class="musicdibs-card bg-base-100">
          <div class="card-body">
            <h2 class="card-title">Añadir proyecto</h2>
            <p>
              Sube una canción ya existente o crea una nueva con ayuda de
              nuestra herramienta de inteligencia artificial
            </p>
            <router-link to="/new_project">
              <button class="btn btn-primary btn-block mt-8 border-0">
                Nuevo proyecto
              </button>
            </router-link>
          </div>
        </div>
      </section>

      <section class="order-3 pt-4 md:order-3 md:col-span-2 md:row-span-3">
        <div class="musicdibs-card bg-base-100">
          <div class="card-body">
            <h2 class="card-title">Ultimos proyectos</h2>
            <p>
              Para todos tus proyectos, ver
              <strong class="link-hover link-primary"
                ><router-link to="/projects">tus proyectos</router-link></strong
              >.
            </p>
            <ul v-if="projectsSummary.length > 0" class="list rounded-box">
              <li v-for="project in projectsSummary" :key="project.id">
                <ProjectListItem
                  :id="project.id"
                  :name="project.name"
                  :isSummary="true"
                  :registrationDate="project.registration?.registered_at"
                />
              </li>
            </ul>
            <p v-else>Todavía no has creado ningún proyecto.</p>
          </div>
        </div>
      </section>

      <section class="order-4 pt-4 md:order-4 md:col-span-2">
        <div class="musicdibs-card secondary bg-base-100">
          <div class="card-body">
            <h2 class="card-title">Ultimos registros</h2>
            <p>
              Para ver todos tus registros, ver
              <strong class="link-hover link-secondary"
                ><router-link to="/projects?filter=registered"
                  >tus proyectos registrados</router-link
                ></strong
              >.
            </p>
            <ul
              v-if="registeredProjectsSummary.length > 0"
              class="list rounded-box"
            >
              <li
                v-for="project in registeredProjectsSummary"
                :key="project.id"
              >
                <ProjectListItem
                  :id="project.id"
                  :name="project.name"
                  :isSummary="true"
                  :registrationDate="project.registration?.registered_at"
                />
              </li>
            </ul>
            <p v-else>Todavía no tienes proyectos registrados.</p>
          </div>
        </div>
      </section>
    </div>
  </div>

  <IdentityModal />
</template>

<script setup>
import { onMounted, computed } from "vue";

import { useProjectsStore } from "../stores/projects.js";
import { useCreditsStore } from "../stores/credits.js";
import { useAuthStore } from "../stores/auth.js";

import SummaryUser from "../components/SummaryUser.vue";
import ProjectListItem from "../components/ProjectListItem.vue";
import IdentityModal from "../components/IdentityModal.vue";

const projectsStore = useProjectsStore();
const creditsStore = useCreditsStore();
const authStore = useAuthStore();

const projectsSummary = computed(() => {
  return projectsStore.projects.slice(0, 10);
});
const registeredProjectsSummary = computed(() => {
  return projectsStore.projects
    .filter((project) => project.registration?.registered_at)
    .slice(0, 10);
});

onMounted(() => {
  projectsStore.fetchProjects({ user_id: authStore.user.id });
  creditsStore.fetchBalance(authStore.user.id);
});
</script>
