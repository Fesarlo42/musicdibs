<template>
  <div>
    <h2 class="card-title">¡Lo hemos encontrado!</h2>
    <p>
      Hemos encontrado el archivo <strong>{{ fileName }}</strong> registrado en:
    </p>
    <ul class="list rounded-box">
      <li class="list-row">
        <div>
          <img
            class="size-10 rounded-box"
            src="../assets/images/musicdibs_icon_350.png"
          />
        </div>
        <div>
          <div>{{ registrationData.project.author }}</div>
          <div class="text-xs font-semibold uppercase opacity-60">
            {{ registrationData.project.name }}
          </div>
        </div>
        <button class="btn btn-primary btn-outline btn-sm ml-auto p-4">
          <span class="hidden sm:inline">Descargar comprobante</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2.0"
            stroke="currentColor"
            class="size-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"
            />
          </svg>
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  registrationData: {
    type: Object,
    required: true,
  },
  fileName: {
    type: String,
    required: true,
  },
});
</script>
