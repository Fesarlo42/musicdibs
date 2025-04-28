<template>
  <div class="musicdibs-card w-full bg-base-100 sm:w-4/5">
    <div class="card-body">
      <h2 class="card-title">Sube tu archivo</h2>
      <fieldset class="fieldset my-6">
        <input
          type="file"
          class="primary-content file-input file-input-primary block w-full"
          @change="onFileChange"
        />
        <p class="label" :class="{ hidden: !showWarning }">
          Por favor, selecciona un archivo antes de continuar.
        </p>
      </fieldset>
      <button class="btn btn-primary" @click="handleUpload">Guardar</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["uploadFile"]);

const file = ref(null);
const showWarning = ref(false);

const onFileChange = (event) => {
  showWarning.value = false;
  file.value = event.target.files[0];
};

const handleUpload = async () => {
  if (file.value === null) {
    showWarning.value = true;
    return;
  }

  emit("uploadFile", file.value);
};
</script>
