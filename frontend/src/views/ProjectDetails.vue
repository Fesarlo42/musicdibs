<!-- ProjectPage.vue -->
<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Detalles del Proyecto</h1>

    <section
      v-if="
        useProjectsStore.error ||
        useGenresStore.error ||
        useRegistrationsStore.error
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
        v-if="useRegistrationsStore.error"
        role="alert"
        class="alert alert-soft alert-error"
      >
        <span>{{ useRegistrationsStore.error }}</span>
      </div>
    </section>

    <ProjectInfo
      class="my-10"
      v-if="project"
      :project="project"
      :editable="!isRegistered"
      :allGenres="allGenres"
      :fileDownloadUrl="fileDownload"
      :isLoading="projectsStore.isLoading"
      @saveForm="handleUpdateProject"
      @saveFile="handleNewFile"
      @deleteFile="handleDeleteFile"
    />

    <ProjectAiAssistant class="my-10" v-if="showAiChat" :project="project" />

    <ProjectRegistration
      class="my-10"
      :isRegistered="isRegistered"
      :registration="ibsRegistration"
      :reciptDownload="reciptDownload"
      :isLoading="registrationsStore.isLoading"
      @registerProject="handleRegisterProject"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useProjectsStore } from "../stores/projects.js";
import { useGenresStore } from "../stores/genres.js";
import { useRegistrationsStore } from "../stores/registrations.js";
import { useAuthStore } from "../stores/auth.js";

import ProjectInfo from "../components/ProjectInfo.vue";
import ProjectRegistration from "../components/ProjectRegistration.vue";
import ProjectAiAssistant from "../components/ProjectAiAssistant.vue";

const projectsStore = useProjectsStore();
const genresStore = useGenresStore();
const registrationsStore = useRegistrationsStore();
const authStore = useAuthStore();

const route = useRoute();
const router = useRouter();

// reactive variables
const userId = ref(null);
const project = ref(null);
const projectFilesDownloadData = ref([]);
const allGenres = ref([]);

// computed properties
const isRegistered = computed(
  () => project.value?.registration?.registered_at != null,
);
const isProjectOwner = computed(() => {
  return project.value.user_id == userId.value;
});
const ibsRegistration = computed(() => {
  return registrationsStore.registration?.evidence_details;
});
const reciptDownload = computed(() => {
  const reciptData = projectFilesDownloadData.value.find(
    (file) => file.origin === "receipt",
  );

  if (!reciptData) {
    return "";
  }

  return reciptData.download_url ? reciptData.download_url : "";
});
const fileDownload = computed(() => {
  const fileData = projectFilesDownloadData.value.find(
    (file) => file.origin !== "receipt",
  );

  if (!fileData) {
    return "";
  }

  return fileData.download_url ? fileData.download_url : "";
});
const showAiChat = computed(() => false); // TODO: Implement AI chat logic

onMounted(async () => {
  const ref = route.params.ref;
  if (ref) {
    project.value = await projectsStore.fetchProjectById(ref);
  } else {
    console.error("Missing project ref in route params");
  }

  userId.value = authStore.user.id;

  if (!isProjectOwner.value) {
    router.push({ name: "Unauthorized" });
    return;
  }

  allGenres.value = await genresStore.fetchAllGenres();

  await getFilesDownloadData();

  await registrationsStore.getRegistration(projectsStore.currentProject.id);
});

const getFilesDownloadData = async () => {
  for (let file of projectsStore.currentProject.files) {
    const downloadedFile = await projectsStore.downloadFile(file.id);

    if (projectsStore.error) {
      console.error("Error downloading file:", projectsStore.error);
      continue;
    }

    projectFilesDownloadData.value.push({
      ...file,
      download_url: downloadedFile.data.download_url,
    });
  }
};

const handleUpdateProject = async (updatedData) => {
  console.log("updating project...", updatedData);
  const payload = {
    name: updatedData.name,
    description: updatedData.description,
    project_genres: updatedData.genres.map((g) => g.id),
  };

  await projectsStore.updateProject(project.value.id, payload);
};

const handleNewFile = async (file) => {
  console.log(file);
};

const handleDeleteFile = async (file) => {
  console.log(file);
};

const handleRegisterProject = async () => {
  await registrationsStore.createRegistration(project.value.id);
};
</script>
