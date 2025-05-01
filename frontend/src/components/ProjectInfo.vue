<template>
  <div class="musicdibs-card bg-base-100">
    <div v-if="isLoading">
      <span class="loading loading-spinner text-primary"></span>
    </div>
    <div v-else class="card-body">
      <h2 class="card-title">Detalles del proyecto</h2>
      <template v-if="project">
        <p v-if="editable">Pincha en la información que deseas editar.</p>
        <div class="grid grid-cols-2 gap-8">
          <div>
            <fieldset class="fieldset">
              <legend class="fieldset-legend">Nombre</legend>
              <div @click="startEditing('name')">
                <template v-if="editingField === 'name'">
                  <input
                    v-model="form.name"
                    class="input"
                    @input="handleInput"
                    @blur="stopEditing"
                    autofocus
                  />
                </template>
                <template v-else>
                  <p class="cursor-pointer">{{ form.name }}</p>
                </template>
              </div>
            </fieldset>

            <fieldset class="fieldset">
              <legend class="fieldset-legend">Descripción</legend>
              <div @click="startEditing('description')">
                <template v-if="editingField === 'description'">
                  <textarea
                    v-model="form.description"
                    class="textarea h-24"
                    @input="handleInput"
                    @blur="stopEditing"
                    autofocus
                  ></textarea>
                </template>
                <template v-else>
                  <p class="cursor-pointer">{{ form.description }}</p>
                </template>
              </div>
            </fieldset>
          </div>

          <div>
            <fieldset class="fieldset">
              <legend class="fieldset-legend">Género</legend>
              <div @click="startEditing('genre')">
                <template v-if="editingField === 'genre'">
                  <div class="flex flex-wrap gap-2">
                    <select
                      v-model="selectedGenre"
                      class="select-bordered select w-full max-w-xs"
                      @change="handleAddGenre"
                    >
                      <option disabled value="">Selecciona un género</option>
                      <option
                        v-for="genreOption in props.allGenres"
                        :key="genreOption.id"
                        :value="genreOption.id"
                      >
                        {{ genreOption.name }}
                      </option>
                    </select>
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
                </template>

                <template v-else>
                  <div class="flex flex-wrap gap-2">
                    <div
                      v-for="(genre, index) in form.genres"
                      :key="genre.id"
                      class="badge badge-soft badge-primary"
                    >
                      {{ genre.name }}
                    </div>
                  </div>
                </template>
              </div>
            </fieldset>

            <fieldset class="fieldset">
              <legend class="fieldset-legend">Subida el</legend>
              <p>{{ userFile?.uploaded_at ? userFile.uploaded_at : "-" }}</p>
            </fieldset>

            <fieldset class="fieldset">
              <legend class="fieldset-legend">Archivo original</legend>
              <div class="flex items-center gap-2">
                <template v-if="userFile">
                  <p>{{ userFile.name || "-" }}</p>
                  <a class="btn btn-ghost btn-sm" :href="fileDownloadUrl">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                      class="size-5"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M12 2.25a.75.75 0 0 1 .75.75v11.69l3.22-3.22a.75.75 0 1 1 1.06 1.06l-4.5 4.5a.75.75 0 0 1-1.06 0l-4.5-4.5a.75.75 0 1 1 1.06-1.06l3.22 3.22V3a.75.75 0 0 1 .75-.75Zm-9 13.5a.75.75 0 0 1 .75.75v2.25a1.5 1.5 0 0 0 1.5 1.5h13.5a1.5 1.5 0 0 0 1.5-1.5V16.5a.75.75 0 0 1 1.5 0v2.25a3 3 0 0 1-3 3H5.25a3 3 0 0 1-3-3V16.5a.75.75 0 0 1 .75-.75Z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </a>

                  <button
                    v-if="editable"
                    class="btn btn-ghost btn-sm text-error"
                    @click="handleDeleteFile"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                      class="size-5"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M16.5 4.478v.227a48.816 48.816 0 0 1 3.878.512.75.75 0 1 1-.256 1.478l-.209-.035-1.005 13.07a3 3 0 0 1-2.991 2.77H8.084a3 3 0 0 1-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 0 1-.256-1.478A48.567 48.567 0 0 1 7.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 0 1 3.369 0c1.603.051 2.815 1.387 2.815 2.951Zm-6.136-1.452a51.196 51.196 0 0 1 3.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 0 0-6 0v-.113c0-.794.609-1.428 1.364-1.452Zm-.355 5.945a.75.75 0 1 0-1.5.058l.347 9a.75.75 0 1 0 1.499-.058l-.346-9Zm5.48.058a.75.75 0 1 0-1.498-.058l-.347 9a.75.75 0 0 0 1.5.058l.345-9Z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </button>
                </template>
                <template v-else>
                  <input
                    type="file"
                    class="primary-content file-input file-input-primary block w-full"
                    @change="handleFileChange"
                  />
                </template>
              </div>
            </fieldset>
          </div>
        </div>

        <div v-if="isChanged" class="mt-6">
          <button class="btn btn-primary" @click="handleSave">
            Guardar cambios
          </button>
        </div>
      </template>
      <template v-else>
        <p class="text-center">
          Hubo un problema al recuperar los datos del proyecto. Vuelve a
          intentar.
        </p>
      </template>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from "vue";

const props = defineProps({
  project: {
    type: Object,
    default: null,
  },
  editable: {
    type: Boolean,
    required: true,
  },
  allGenres: {
    type: Array,
    required: true,
  },
  fileDownloadUrl: {
    type: String,
    default: "",
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["saveForm", "saveFile", "deleteFile"]);

const form = reactive({
  name: props.project?.name || "",
  description: props.project?.description || "",
  genres: props.project?.project_genres
    ? props.project.project_genres.map((pg) => ({
        id: pg.genre.id,
        name: pg.genre.name,
      }))
    : [],
});

const selectedGenre = ref("");
const editingField = ref(null);
const newFile = ref(null);
const isChanged = ref(false);

const userFile = computed(() => {
  return props.project.files.find(
    (file) => file.origin === "user_upload" || file.origin === "ai_generated",
  );
});

onMounted(() => {
  console.log("Project data:", props.project);
  console.log("all genres", props.allGenres);
});

const startEditing = (field) => {
  console.log("Editing field:", field);
  if (!props.editable) return;
  editingField.value = field;
};

const stopEditing = () => {
  editingField.value = null;
};

const handleInput = () => {
  isChanged.value = true;
};

const handleAddGenre = () => {
  if (!selectedGenre.value) return;

  const exists = form.genres.find((g) => g.id === selectedGenre.value);
  if (!exists) {
    const genreData = props.allGenres.find((g) => g.id === selectedGenre.value);
    if (genreData) {
      form.genres.push({
        id: genreData.id,
        name: genreData.name,
      });
      isChanged.value = true;
    }
  }

  selectedGenre.value = "";
};

const handleRemoveGenre = (index) => {
  if (form.genres.length > 1) {
    form.genres.splice(index, 1);
    isChanged.value = true;
  }
};

const handleSave = () => {
  emit("saveForm", { ...form });

  if (newFile.value) {
    emit("saveFile", newFile.value);
  }

  isChanged.value = false;
  stopEditing();
};

const handleFileChange = (event) => {
  isChanged.value = true;
  newFile.value = event.target.files[0];
};

const handleDeleteFile = () => {
  if (userFile.value && props.editable) {
    emit("deleteFile", userFile.value);
    stopEditing();
  }
};
</script>
