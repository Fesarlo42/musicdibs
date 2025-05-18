<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Mis Projectos</h1>
    <section class="mt-4 px-4">
      <div class="musicdibs-card w-full bg-base-100">
        <div class="card-body">
          <h2 class="card-title">Listado de proyectos</h2>
          <p>
            Pincha en el nombre de cada canción para acceder a sus detalles.
          </p>
          <ul v-if="projectsStore.projects.length > 0" class="list rounded-box">
            <li class="flex items-center justify-between p-2">
              <p class="pl-12">Titulo</p>
              <div
                class="flex items-center justify-between text-center md:w-[30%]"
              >
                <p class="px-2">Actualizado en</p>
                <p class="px-2">Registrar</p>
                <p class="px-2">Borrar</p>
              </div>
            </li>
            <li v-for="project in filteredProjects" :key="project.id">
              <ProjectListItem
                :id="project.id"
                :name="project.name"
                :isSummary="false"
                :registrationDate="project.registration?.registered_at"
                :lastUpdated="project.updated_at"
                @registerProject="handleRegister"
                @deleteProject="handleDelete"
              />
            </li>
          </ul>
          <p v-else>Todavía no has creado ningún proyecto.</p>

          <div v-if="projectsStore.pagination.totalPages > 1" class="mt-4 join">
            <button
              v-for="page in projectsStore.pagination.totalPages"
              :key="page"
              @click="goToPage(page)"
              :class="[
                'btn join-item',
                page === projectsStore.pagination.currentPage
                  ? 'btn-active'
                  : '',
              ]"
            >
              {{ page }}
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useProjectsStore } from "../stores/projects.js";
import { useRegistrationsStore } from "../stores/registrations.js";
import { useAuthStore } from "../stores/auth.js";

import ProjectListItem from "../components/ProjectListItem.vue";

const projectsStore = useProjectsStore();
const registrationsStore = useRegistrationsStore();
const authStore = useAuthStore();

const route = useRoute();
const router = useRouter();

// Load projects when component mounts
const loadProjects = async () => {
  const page = Number(route.query.page) || 1;
  await projectsStore.fetchProjects({ user_id: authStore.user.id, page: page });
};

onMounted(() => {
  loadProjects();
});

// Watch if page or filter changes
watch(
  () => [route.query.page, route.query.filter],
  async () => {
    await loadProjects();
  },
);

const filteredProjects = computed(() => {
  const filter = route.query.filter;
  if (filter === "registered") {
    return projectsStore.projects.filter(
      (project) => project.registration?.registered_at,
    );
  }
  return projectsStore.projects;
});

const goToPage = (page) => {
  router.push({ query: { ...route.query, page } });
};

const handleRegister = async (projectId) => {
  const projectData = await projectsStore.fetchProjectById(projectId);

  if (
    projectData?.files?.some(
      (file) => file.origin === "user_upload" || file.origin === "ai_generated",
    )
  ) {
    await registrationsStore.createRegistration(projectId);
    loadProjects();
  } else {
    alert("No se puede registrar proyectos sin archivos.");
  }
};
const handleDelete = async (projectId) => {
  console.log(projectId.projectId);
  let confirm = window.confirm(
    "¿Estás seguro de que quieres eliminar ese proyecto? Esta acción no se puede deshacer.",
  );
  if (confirm) {
    await projectsStore.deleteProject(projectId.projectId);
  }
};
</script>
