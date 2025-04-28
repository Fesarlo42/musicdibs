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

import ProjectNewForm from "../components/ProjectNewForm.vue";
import ProjectNewFile from "../components/ProjectNewFile.vue";
import ProjectNewAi from "../components/ProjectNewAi.vue";

const genresStore = useGenresStore();
const projectsStore = useProjectsStore();
const router = useRouter();

const userId = ref(null);
const newProjectId = ref(null);
const allGenres = ref([]);
const showUploadFileCard = ref(false);
const showAiCard = ref(false);

onMounted(async () => {
  const userData = JSON.parse(sessionStorage.getItem("user"));
  userId.value = userData.id;

  allGenres.value = await genresStore.fetchAllGenres();
});

const createProject = async (projectData) => {
  // TODO: porque no funciona?!
  console.log("projectData: ", projectData);
  console.log("project vlue: ", projectData.value);
  console.log("project name: ", projectData.name);
  const payload = {
    name: projectData.value.name,
    description: projectData.value.description,
    user_id: userId.value,
    project_genres: projectData.value.genres.map((g) => g.id),
  };

  const createdProject = await projectsStore.createProject(payload);

  if (!createdProject || !createdProject.id) {
    return;
  }
  newProjectId.value = createdProject.id;

  if (projectData.value.projectType === "existing") {
    showUploadFileCard.value = true;
  } else if (projectData.value.projectType === "new") {
    showAiCard.value = true;
  }
};

const uploadProjectFile = async (file) => {
  if (!newProjectId) {
    console.log("No project id to upload file");
    return;
  }

  await projectsStore.uploadProjectFile(newProjectId, file);

  router.push(`/projects/${newProjectId}`);
};

const createConversation = async (conversationData) => {
  // TODO: esse provavelmente não funciona também
  const payload = {
    purpose: conversationData.value.purpose,
    tempo: conversationData.value.tempo,
    key_signature: conversationData.value.key_signature,
    mood: conversationData.value.mood,
    status: "in_progress",
  };

  await projectsStore.createConversation(newProjectId.value, payload);

  if (projectsStore.error) {
    return;
  }

  router.push(`/projects/${newProjectId}`);
};
</script>
