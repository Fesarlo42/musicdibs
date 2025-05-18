<template>
  <div class="musicdibs-card secondary bg-base-100">
    <div v-if="isLoading">
      <span class="loading loading-spinner text-secondary"></span>
    </div>
    <div v-else class="card-body">
      <template v-if="isRegistered">
        <h2 class="card-title">Detalles del registro</h2>

        <div
          v-if="registration && registration?.status == 'certified'"
          class="grid-cols-3 grid-rows-5 gap-4 md:grid"
        >
          <fieldset class="fieldset">
            <legend class="fieldset-legend">UUID</legend>
            <p class="break-all">{{ registration?.id || "-" }}</p>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Registrado el</legend>
            <p class="break-all">
              {{ registration?.certification.timestamp || "-" }}
            </p>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Estado</legend>
            <p
              class="badge badge-secondary"
              :class="{ 'badge-soft': registration?.status !== 'certified' }"
            >
              {{ registration?.status || "-" }}
            </p>
          </fieldset>

          <fieldset class="fieldset">
            <legend class="fieldset-legend">Archivo</legend>
            <p class="break-all">
              {{ registration?.payload.integrity[0].name || "-" }}
            </p>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Algorimo</legend>
            <p class="break-all">
              {{ registration?.payload.integrity[0].algorithm || "-" }}
            </p>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Codificado en</legend>
            <p class="break-all">
              {{ registration?.payload.integrity[0].sanitizer || "-" }}
            </p>
          </fieldset>

          <fieldset class="fieldset col-span-3">
            <legend class="fieldset-legend">Codigo de integridad</legend>
            <p class="break-all">
              {{ registration?.payload.integrity[0].checksum || "-" }}
            </p>
          </fieldset>

          <fieldset class="fieldset">
            <legend class="fieldset-legend">Red blockchain</legend>
            <p class="break-all">
              {{ registration?.certification.network || "" }}
            </p>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Timestamp</legend>
            <p class="break-all">
              {{ registration?.certification.timestamp || "-" }}
            </p>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Verificar</legend>
            <a
              class="link-hover link-secondary"
              target="_blank"
              :href="registration?.certification.links.checker"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                fill="currentColor"
                class="size-6"
              >
                <path
                  d="M6.22 8.72a.75.75 0 0 0 1.06 1.06l5.22-5.22v1.69a.75.75 0 0 0 1.5 0v-3.5a.75.75 0 0 0-.75-.75h-3.5a.75.75 0 0 0 0 1.5h1.69L6.22 8.72Z"
                />
                <path
                  d="M3.5 6.75c0-.69.56-1.25 1.25-1.25H7A.75.75 0 0 0 7 4H4.75A2.75 2.75 0 0 0 2 6.75v4.5A2.75 2.75 0 0 0 4.75 14h4.5A2.75 2.75 0 0 0 12 11.25V9a.75.75 0 0 0-1.5 0v2.25c0 .69-.56 1.25-1.25 1.25h-4.5c-.69 0-1.25-.56-1.25-1.25v-4.5Z"
                />
              </svg>
            </a>
          </fieldset>

          <fieldset class="fieldset col-span-2">
            <legend class="fieldset-legend">Hash</legend>
            <p class="break-all">
              {{ registration?.certification.hash || "-" }}
            </p>
          </fieldset>
          <div class="btn btn-secondary btn-sm mt-4 self-center">
            <a :href="reciptDownload" target="_blank">Descargar comprobante</a>
          </div>
        </div>
        <div v-else class="grid-cols-3 gap-4 md:grid">
          <fieldset class="fieldset">
            <legend class="fieldset-legend">UUID</legend>
            <p>{{ registration?.id || "-" }}</p>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Registrado el</legend>
            <p>
              {{ registration?.certification.timestamp || "-" }}
            </p>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Estado</legend>
            <p
              class="badge badge-secondary"
              :class="{ 'badge-soft': registration?.status !== 'certified' }"
            >
              {{ registration?.status || "-" }}
            </p>
          </fieldset>
        </div>
      </template>
      <template v-else>
        <h2 class="card-title">Registrar proyecto</h2>
        <p>
          Pincha el botón abajo para registrar tu proyecto. Una vez registrado,
          ya no se podrán hacer cambios a este proyecto, así que revisalo bien.
        </p>
        <button
          class="btn btn-secondary btn-wide mt-6"
          @click="registerProject"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            class="size-6"
          >
            <path
              fill-rule="evenodd"
              d="M12.516 2.17a.75.75 0 0 0-1.032 0 11.209 11.209 0 0 1-7.877 3.08.75.75 0 0 0-.722.515A12.74 12.74 0 0 0 2.25 9.75c0 5.942 4.064 10.933 9.563 12.348a.749.749 0 0 0 .374 0c5.499-1.415 9.563-6.406 9.563-12.348 0-1.39-.223-2.73-.635-3.985a.75.75 0 0 0-.722-.516l-.143.001c-2.996 0-5.717-1.17-7.734-3.08Zm3.094 8.016a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z"
              clip-rule="evenodd"
            />
          </svg>

          Registrar proyecto
        </button>
      </template>
    </div>
  </div>
</template>
<script setup>
import { onMounted } from "vue";

const props = defineProps({
  isRegistered: {
    type: Boolean,
    required: true,
  },
  isLoading: {
    type: Boolean,
  },
  registration: {
    type: Object,
    default: null,
  },
  reciptDownload: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["registerProject"]);

const registerProject = () => {
  emit("registerProject");
};

onMounted(() => {
  console.log("project registration", props.registration);
});
</script>
