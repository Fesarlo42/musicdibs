<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Detalles del Proyecto</h1>

    <section
      v-if="
        useProjectsStore.error ||
        useGenresStore.error ||
        useRegistrationsStore.error ||
        localError
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
      <div v-if="localError" role="alert" class="alert alert-soft alert-error">
        <span>{{ localError }}</span>
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

    <ProjectRegistration
      v-if="hasUploadableFiles"
      class="my-10"
      :isRegistered="isRegistered"
      :registration="ibsRegistration"
      :reciptDownload="reciptDownload"
      :isLoading="registrationsStore.isLoading"
      @registerProject="handleRegisterProject"
    />

    <ProjectAiAssistant
      class="my-10"
      v-if="showAiChat"
      :project="project"
      :messages="conversationsStore.messages"
      :isLoading="conversationsStore.loading"
      :status="conversationStatus"
      @sendMessage="handleSendMessage"
      @finishConversation="handleFinishConversation"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useProjectsStore } from "../stores/projects.js";
import { useGenresStore } from "../stores/genres.js";
import { useRegistrationsStore } from "../stores/registrations.js";
import { useAuthStore } from "../stores/auth.js";
import { useConversationsStore } from "../stores/conversations.js";

import ProjectInfo from "../components/ProjectInfo.vue";
import ProjectRegistration from "../components/ProjectRegistration.vue";
import ProjectAiAssistant from "../components/ProjectAiAssistant.vue";

const projectsStore = useProjectsStore();
const genresStore = useGenresStore();
const registrationsStore = useRegistrationsStore();
const authStore = useAuthStore();
const conversationsStore = useConversationsStore();

const route = useRoute();
const router = useRouter();

// reactive variables
const userId = ref(null);
const project = ref(null);
const projectFilesDownloadData = ref([]);
const allGenres = ref([]);
const showAiChat = ref(null);
const conversationId = ref(null);
const localError = ref(null);

// computed properties
const isRegistered = computed(() => project.value?.registration?.id != null);
const isProjectOwner = computed(() => {
  return project.value?.user_id == userId.value;
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
const hasUploadableFiles = computed(() =>
  project.value?.files?.some(
    (file) => file.origin === "user_upload" || file.origin === "ai_generated",
  ),
);
const conversationStatus = computed(
  () => conversationsStore.currentConversation?.status || null,
);

onMounted(async () => {
  const ref = route.params.ref;
  if (ref) {
    project.value = await projectsStore.fetchProjectById(ref);
  } else {
    console.error("Missing project ref in route params");
    return;
  }

  userId.value = authStore.user.id;

  if (!isProjectOwner.value) {
    router.push({ name: "Unauthorized" });
    return;
  }

  allGenres.value = await genresStore.fetchAllGenres();

  await getFilesDownloadData();

  showAiChat.value = await projectsStore.fetchConversation(project.value.id);
  if (showAiChat.value && showAiChat.value.id) {
    conversationId.value = showAiChat.value.id;
    await conversationsStore.fetchMessages(conversationId.value);
    await conversationsStore.getConversation(conversationId.value);
  }

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
  await projectsStore.uploadProjectFile(project.value.id, file);
  project.value = await projectsStore.fetchProjectById(project.value.id);
};

const handleDeleteFile = async (file) => {
  let confirm = window.confirm(
    "¿Estas seguro que desas borrar el archivo? Esta acción no se puede deshacer",
  );

  if (confirm) {
    await projectsStore.deleteProjectFile(file.id);
    project.value = await projectsStore.fetchProjectById(project.value.id);
  }
};

const handleRegisterProject = async () => {
  if (hasUploadableFiles) {
    await registrationsStore.createRegistration(project.value.id);
    project.value = await projectsStore.fetchProjectById(project.value.id);
  } else {
    localError.value(
      "No puedes hacer registros sin ningun archivo. Por favo, sube o genera un archivo con nuestro asistente AI.",
    );
  }
};

const handleSendMessage = async (message) => {
  if (conversationId.value) {
    await conversationsStore.generateMessage({
      conversation_id: conversationId.value,
      user_message: message,
    });
    await conversationsStore.getConversation(conversationId.value);
  }
};

const handleFinishConversation = async () => {
  if (conversationId.value) {
    await conversationsStore.finishConversation(conversationId.value);
    await conversationsStore.getConversation(conversationId.value);
    showAiChat.value = null;
  }
};
</script>
