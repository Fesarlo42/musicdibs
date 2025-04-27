<!-- ProjectPage.vue -->
<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Detalles del Proyecto</h1>

    <ProjectInfo
      class="my-10"
      v-if="project"
      :project="project"
      :editable="!isRegistered"
      :allGenres="genresStore.genres"
      :fileDownloadUrl="fileDownload"
      :isLoading="projectsStore.isLoading"
      @saveForm="handleUpdateProject"
      @saveFile="handleNewFile"
    />

    <ProjectRegistration
      class="my-10"
      v-if="isRegistered"
      :registration="ibsRegistration"
      :reciptDownload="reciptDownload"
      :isLoading="registrationsStore.isLoading"
    />

    <ProjectAiAssistant class="my-10" v-if="showAiChat" :project="project" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useProjectsStore } from "../stores/projects.js";
import { useGenresStore } from "../stores/genres.js";
import { useRegistrationsStore } from "../stores/registrations.js";

import ProjectInfo from "../components/ProjectInfo.vue";
import ProjectRegistration from "../components/ProjectRegistration.vue";
import ProjectAiAssistant from "../components/ProjectAiAssistant.vue";

const projectsStore = useProjectsStore();
const genresStore = useGenresStore();
const registrationsStore = useRegistrationsStore();

const route = useRoute();
const router = useRouter();

// reactive variables
const project = ref(null);
const projectFilesDownloadData = ref([]);
const ibsRegistration = ref(null);

// computed properties
const isRegistered = computed(
  () => project.value?.registration?.registered_at != null,
);
const isProjectOwner = computed(() => {
  const userId = projectsStore.userId;
  return project.value?.owner_id === userId;
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
  if (!isProjectOwner.value) {
    router.push({ name: "Unauthorized" });
    return;
  }

  const ref = route.params.ref;
  if (ref) {
    project.value = await projectsStore.fetchProjectById(ref);
  } else {
    console.error("Missing project ref in route params");
  }

  await genresStore.fetchAllGenres();

  await getFilesDownloadData();

  await registrationsStore.getRegistration(projectsStore.currentProject.id);

  ibsRegistration.value = registrationsStore.registration?.evidence_details;
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
  // call your store to update project
};

const handleNewFile = async (file) => {
  // call your store to upload file
};
</script>
