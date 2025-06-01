<template>
  <div class="musicdibs-card w-full bg-base-100 sm:w-4/5">
    <div class="card-body">
      <h2 class="card-title">Describe tu nueva obra</h2>
      <p>Cuanto más detalles nos des, mejor será el resultado del asistente.</p>
      <div class="grid-cols-2 gap-8 md:grid">
        <div>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Objetivo del proyecto</legend>
            <input
              v-model="form.purpose"
              placeholder="Letra de canción, partitura, etc..."
              class="input"
              autofocus
            />
          </fieldset>

          <fieldset class="fieldset">
            <legend class="fieldset-legend">Tempo de la obra (en BPM)</legend>
            <input v-model="form.tempo" class="input" autofocus />
          </fieldset>
        </div>

        <div>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Armadura de tonalidad</legend>
            <input v-model="form.key_signature" class="input" autofocus />
          </fieldset>

          <fieldset class="fieldset">
            <legend class="fieldset-legend">
              Estado de ánimo o <i>mood</i> de la obra
            </legend>
            <input v-model="form.mood" class="input" autofocus />
          </fieldset>

          <div class="mt-10 flex justify-end gap-4">
            <button class="btn btn-primary" @click="handleSubmit">
              Guardar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const form = ref({
  purpose: "",
  tempo: "",
  key_signature: "",
  mood: "",
});

const emit = defineEmits(["createConversation"]);

const handleSubmit = () => {
  emit("createConversation", { ...form.value });
};
</script>
