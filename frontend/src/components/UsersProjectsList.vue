<template>
  <ul v-if="projectsStore.projects.length > 0" class="list rounded-box">
    <li class="flex items-center justify-between p-2">
      <p class="pl-12">Titulo</p>
      <p class="pl-12 text-center">Registrado el</p>
    </li>
    <li v-for="project in filteredProjects" :key="project.id">
      <ProjectListItem
        :id="project.id"
        :name="project.name"
        :isSummary="false"
        :isAdmin="true"
        :registrationDate="project.registration?.registered_at"
        :lastUpdated="project.updated_at"
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
        page === projectsStore.pagination.currentPage ? 'btn-active' : '',
      ]"
    >
      {{ page }}
    </button>
  </div>
</template>

<script setup>
import { onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useProjectsStore } from "../stores/projects.js";

import ProjectListItem from "../components/ProjectListItem.vue";

// Define props
const props = defineProps({
  userId: {
    type: [String, Number],
    required: true,
  },
});

const projectsStore = useProjectsStore();

const route = useRoute();
const router = useRouter();

// Load projects when component mounts
const loadProjects = async () => {
  const page = Number(route.query.page) || 1;
  await projectsStore.fetchProjects({ user_id: props.userId, page: page });
};

onMounted(() => {
  loadProjects();
});

// Watch if page or filter changes, or userId prop changes
watch(
  () => [route.query.page, route.query.filter, props.userId],
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
</script>
