<template>
  <router-link
    v-if="isSummary"
    :to="`/projects/${id}`"
    class="list-row cursor-pointer rounded-box p-2 transition-colors hover:bg-gray-100"
  >
    <div>
      <img
        v-if="registrationDate"
        class="size-10 rounded-box"
        src="../assets/images/certif_ok_morado.png"
      />
      <img
        v-else
        class="size-10 rounded-box"
        src="../assets/images/certif_ok_rosa.png"
      />
    </div>
    <div>
      <div
        class="text-xs font-semibold uppercase"
        :class="registrationDate ? 'text-secondary' : 'text-primary'"
      >
        {{ name }}
      </div>
      <div v-if="registrationDate" class="text-xs">
        Certificado en {{ formattedDate }}
      </div>
    </div>
    <div>
      <div v-if="registrationDate" class="secondary p-4">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="var(--color-secondary)"
          class="secondary size-6"
        >
          <path
            fill-rule="evenodd"
            d="M12.516 2.17a.75.75 0 0 0-1.032 0 11.209 11.209 0 0 1-7.877 3.08.75.75 0 0 0-.722.515A12.74 12.74 0 0 0 2.25 9.75c0 5.942 4.064 10.933 9.563 12.348a.749.749 0 0 0 .374 0c5.499-1.415 9.563-6.406 9.563-12.348 0-1.39-.223-2.73-.635-3.985a.75.75 0 0 0-.722-.516l-.143.001c-2.996 0-5.717-1.17-7.734-3.08Zm3.094 8.016a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
    </div>
  </router-link>

  <li v-else class="list-row rounded-box p-2">
    <div>
      <img
        v-if="registrationDate"
        class="size-10 rounded-box"
        src="../assets/images/certif_ok_morado.png"
      />
      <img
        v-else
        class="size-10 rounded-box"
        src="../assets/images/certif_ok_rosa.png"
      />
    </div>
    <div>
      <router-link
        :to="`/projects/${id}`"
        :class="
          registrationDate
            ? 'link-hover link-secondary'
            : 'link-hover link-primary'
        "
      >
        <div
          class="text-xs font-semibold uppercase"
          :class="registrationDate ? 'text-secondary' : 'text-primary'"
        >
          {{ name }}
        </div>
        <div v-if="registrationDate">Certificado en {{ formattedDate }}</div>
      </router-link>
    </div>
    <div class="mx-5 flex items-center">{{ formattedLastUpdated }}</div>
    <div class="flex items-center">
      <button
        v-if="!registrationDate && handleRegistration"
        class="btn btn-primary btn-outline btn-sm ml-auto p-4"
        @click="handleRegistration"
      >
        <span class="hidden sm:inline">Registrar</span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="var(--color-gray-200)"
          class="primary size-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z"
          />
        </svg>
      </button>
      <div v-else-if="registrationDate" class="scondary p-4">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="var(--color-secondary)"
          class="secondary size-6"
        >
          <path
            fill-rule="evenodd"
            d="M12.516 2.17a.75.75 0 0 0-1.032 0 11.209 11.209 0 0 1-7.877 3.08.75.75 0 0 0-.722.515A12.74 12.74 0 0 0 2.25 9.75c0 5.942 4.064 10.933 9.563 12.348a.749.749 0 0 0 .374 0c5.499-1.415 9.563-6.406 9.563-12.348 0-1.39-.223-2.73-.635-3.985a.75.75 0 0 0-.722-.516l-.143.001c-2.996 0-5.717-1.17-7.734-3.08Zm3.094 8.016a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
    </div>
  </li>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  id: {
    type: Number,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  isSummary: {
    type: Boolean,
    default: false,
    required: false,
  },
  handleRegistration: {
    type: Function,
    default: null,
    required: false,
  },
  registrationDate: {
    type: String,
    default: null,
    required: false,
  },
  lastUpdated: {
    type: String,
    default: null,
    required: false,
  },
});

const formattedDate = computed(() => {
  if (!props.registrationDate) return "";
  return new Date(props.registrationDate).toLocaleDateString();
});
const formattedLastUpdated = computed(() => {
  if (!props.lastUpdated) return "";
  const date = new Date(props.lastUpdated);
  return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
});
</script>
