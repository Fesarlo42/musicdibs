<template>
  <div class="musicdibs-card w-fullbg-base-100 sm:w-4/5">
    <div class="card-body">
      <h2 class="card-title">Detalles del proyecto</h2>

      <div class="grid grid-cols-2 gap-8">
        <div>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Nombre del proyecto</legend>
            <input
              v-model="form.name"
              class="validator input"
              required
              autofocus
            />
            <div class="validator-hint hidden">
              El nombre no puede estar vacío
            </div>
          </fieldset>

          <fieldset class="fieldset">
            <legend class="fieldset-legend">Descripción</legend>
            <textarea
              v-model="form.description"
              class="textarea h-24"
            ></textarea>
          </fieldset>
        </div>

        <div>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Género del proyecto</legend>
            <div class="flex flex-wrap gap-2">
              <select
                v-model="selectedGenre"
                class="select-bordered select w-full max-w-xs"
                required
                @change="handleAddGenre"
              >
                <option disabled value="">
                  Selecciona los géneros del proyecto
                </option>
                <option
                  v-for="genreOption in allGenres"
                  :key="genreOption.id"
                  :value="genreOption.id"
                >
                  {{ genreOption.name }}
                </option>
              </select>
              <div class="validator-hint" :class="{ hidden: !genreInvalid }">
                Por favor selecciona al menos un género
              </div>

              <div class="mt-4 flex flex-wrap gap-2">
                <div
                  v-for="(genre, index) in form.genres"
                  :key="genre.id"
                  class="badge badge-soft badge-primary"
                >
                  {{ genre.name }}
                  <button
                    v-if="form.genres.length > 1"
                    class="btn btn-ghost btn-sm"
                    @click.stop="handleRemoveGenre(index)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 16 16"
                      fill="currentColor"
                      class="size-4"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14Zm2.78-4.22a.75.75 0 0 1-1.06 0L8 9.06l-1.72 1.72a.75.75 0 1 1-1.06-1.06L6.94 8 5.22 6.28a.75.75 0 0 1 1.06-1.06L8 6.94l1.72-1.72a.75.75 0 1 1 1.06 1.06L9.06 8l1.72 1.72a.75.75 0 0 1 0 1.06Z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </fieldset>

          <fieldset class="fieldset">
            <legend class="fieldset-legend">Vais a...</legend>
            <p class="flex items-center gap-2">
              <input
                type="radio"
                class="radio radio-primary"
                value="existing"
                v-model="form.projectType"
              />
              <span class="label-text">Registrar una obra ya existente</span>
            </p>

            <p class="flex items-center gap-2">
              <input
                type="radio"
                class="radio radio-primary"
                value="new"
                v-model="form.projectType"
              />
              <span class="label-text">Crear una nueva obra y registrarla</span>
            </p>

            <div
              class="validator-hint"
              :class="{ hidden: !projectTypeInvalid }"
            >
              Por favor selecciona una opción
            </div>
          </fieldset>

          <div class="mt-10 flex justify-end gap-4">
            <button class="btn btn-primary" @click="handleSubmit">
              Crear proyecto
            </button>
            <button class="btn btn-primary btn-soft" @click="handleCancel">
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  allGenres: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["createProject"]);

const selectedGenre = ref("");
const form = ref({
  name: "",
  description: "",
  genres: [],
  projectType: "",
});

const genreInvalid = computed(() => {
  return form.value.genres.length === 0;
});
const projectTypeInvalid = computed(() => {
  return !form.value.projectType;
});

// Handlers
const handleAddGenre = () => {
  const foundGenre = props.allGenres.find((g) => g.id === selectedGenre.value);
  if (foundGenre && !form.value.genres.some((g) => g.id === foundGenre.id)) {
    form.value.genres.push({
      id: foundGenre.id,
      name: foundGenre.name,
    });
  }
  selectedGenre.value = "";
};

const handleRemoveGenre = (index) => {
  form.value.genres.splice(index, 1);
};

const handleCancel = () => {
  form.value = {
    name: "",
    description: "",
    genres: [],
    projectType: "",
  };
};

const handleSubmit = () => {
  console.log("createProject", form);
  emit("createProject", { ...form });
};
</script>
