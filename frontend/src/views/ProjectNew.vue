<template>
  <h1 class="text-2xl font-bold">Nuevo proyecto</h1>
  <section
    v-if="
      useProjectsStore.error ||
      useGenresStore.error ||
      useCreditsStore.error ||
      useConversationsStore.error
    "
  >
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
    <div
      v-if="useCreditsStore.error"
      role="alert"
      class="alert alert-soft alert-error"
    >
      <span>{{ useCreditsStore.error }}</span>
    </div>
    <div
      v-if="useConversationsStore.error"
      role="alert"
      class="alert alert-soft alert-error"
    >
      <span>{{ useConversationsStore.error }}</span>
    </div>
  </section>

  <section
    v-if="creditsStore.balance && creditsStore.balance > 0"
    class="my-10 flex justify-center py-10"
  >
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

  <section v-else class="my-10 flex justify-center py-10">
    <div class="musicdibs-card bg-base-100">
      <div class="card-body">
        <h2 class="card-title">¡No tienes créditos!</h2>
        <p>No tienes créditos suficientes para crear un nuevo proyecto.</p>
        <p>Para obtener más créditos, contacta con un administrador.</p>
        <router-link to="/dashboard">
          <button class="btn btn-primary btn-block mt-8 border-0">
            Volver al dashboard
          </button>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import { useGenresStore } from "../stores/genres.js";
import { useProjectsStore } from "../stores/projects.js";
import { useAuthStore } from "../stores/auth.js";
import { useCreditsStore } from "../stores/credits.js";
import { useConversationsStore } from "../stores/conversations.js";

import ProjectNewForm from "../components/ProjectNewForm.vue";
import ProjectNewFile from "../components/ProjectNewFile.vue";
import ProjectNewAi from "../components/ProjectNewAi.vue";

const genresStore = useGenresStore();
const projectsStore = useProjectsStore();
const authStore = useAuthStore();
const creditsStore = useCreditsStore();
const conversationsStore = useConversationsStore();

const router = useRouter();

const userId = ref(null);
const newProjectId = ref(null);
const allGenres = ref([]);
const showUploadFileCard = ref(false);
const showAiCard = ref(false);

onMounted(async () => {
  userId.value = authStore.user.id;

  allGenres.value = await genresStore.fetchAllGenres();
  await creditsStore.fetchBalance(userId.value);
});

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

  // subtract a credit from the user
  await creditsStore.removeCredits(userId.value, 1);

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
    project_id: newProjectId.value,
  };

  await conversationsStore.createConversation(payload);

  if (conversationsStore.error) {
    return;
  }

  router.push(`/projects/${newProjectId.value}`);
};
</script>
