<template>
  <h1 class="text-2xl font-bold">Nuevo proyecto</h1>
  <section v-if="useProjectsStore.error || useGenresStore.error">
    <div
      v-if="useProjectsStore.error"
      role="alert"
      class="alert alert-soft alert-error"
    >
      <span>{{ useProjectsStore.error }}</span>
    </div>
    <div
      v-if="useGenresStore.error"
      role="alert"
      class="alert alert-soft alert-error"
    >
      <span>{{ useGenresStore.error }}</span>
    </div>
  </section>

  <section class="my-10 flex justify-center py-10">
    <template v-if="!showUploadFileCard && !showAiCard">
      <ProjectNewForm :allGenres="allGenres" @createProject="createProject" />
    </template>

    <template v-else-if="showUploadFileCard">
      <ProjectNewFile @uploadFile="uploadProjectFile" />
    </template>

    <template v-else-if="showAiCard">
      <ProjectNewAi @createConversation="createConversation" />
    </template>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";

import { useGenresStore } from "../stores/genres.js";
import { useProjectsStore } from "../stores/projects.js";
import { useAuthStore } from "../stores/auth.js";

import ProjectNewForm from "../components/ProjectNewForm.vue";
import ProjectNewFile from "../components/ProjectNewFile.vue";
import ProjectNewAi from "../components/ProjectNewAi.vue";

const genresStore = useGenresStore();
const projectsStore = useProjectsStore();
const authStore = useAuthStore();
const router = useRouter();

const userId = ref(null);
const newProjectId = ref(null);
const allGenres = ref([]);
const showUploadFileCard = ref(false);
const showAiCard = ref(false);

onMounted(async () => {
  const userData = JSON.parse(sessionStorage.getItem("user"));
  userId.value = authStore.user.id;

  allGenres.value = await genresStore.fetchAllGenres();
});

// TODO: check credits and subtract credits or give error if user doesnt have enought
const createProject = async (projectData) => {
  const payload = {
    name: projectData.name,
    description: projectData.description,
    user_id: userId.value,
    project_genres: projectData.genres.map((g) => g.id),
  };

  const createdProject = await projectsStore.createProject(payload);

  if (!createdProject || !createdProject.id) {
    return;
  }
  newProjectId.value = createdProject.id;

  if (projectData.projectType === "existing") {
    showUploadFileCard.value = true;
  } else if (projectData.projectType === "new") {
    showAiCard.value = true;
  }
};

const uploadProjectFile = async (file) => {
  if (!newProjectId.value) {
    console.log("No project id to upload file");
    return;
  }

  await projectsStore.uploadProjectFile(newProjectId.value, file);

  router.push(`/projects/${newProjectId.value}`);
};

const createConversation = async (conversationData) => {
  const payload = {
    purpose: conversationData.purpose,
    tempo: conversationData.tempo,
    key_signature: conversationData.key_signature,
    mood: conversationData.mood,
    status: "in_progress",
  };

  await projectsStore.createConversation(newProjectId.value, payload);

  if (projectsStore.error) {
    return;
  }

  router.push(`/projects/${newProjectId}`);
};
</script>
