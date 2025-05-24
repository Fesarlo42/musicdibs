<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Verificar obra</h1>
    <section class="my-10 px-4 py-10">
      <div class="musicdibs-card w-full bg-base-100 sm:w-3/5">
        <div
          v-if="registrationsStore.error"
          role="alert"
          class="alert alert-soft alert-error"
        >
          <span>{{ registrationsStore.error }}</span>
        </div>
        <div class="card-body" v-if="registrationsStore.verification">
          <div v-if="registrationsStore.verification.status == 'failure'">
            <h2 class="card-title">Lo sentimos</h2>
            <p>
              El archivo <strong>{{ fileName }}</strong> que has intentado
              verificar no consta como registrado y certificado por nosotros.
              También puede ser que este archivo NO sea el original que se
              registró en su momento. Si quieres registrarlo, vete a tu panel
              general o crea una cuenta gratis y registra esta y muchas otras
              obras.
            </p>
            <button class="btn btn-primary btn-soft mt-5" @click="handleReset">
              Verificar otro archivo
            </button>
          </div>
          <div v-else>
            <FileFound
              :registrationData="registrationsStore.verification"
              :fileName="fileName"
            />
            <button
              class="btn btn-secondary btn-soft mt-5"
              @click="handleReset"
            >
              Verificar otro archivo
            </button>
          </div>
        </div>
        <div class="card-body" v-else>
          <h2 class="card-title">Subir archivo</h2>
          <p>
            Comprueba si una obra ya ha sido registrada previamente
            en Musicdibs o no.
          </p>
          <p>
            Tan solo selecciona el archivo original que se ha registrado
            con Musicdibs y pulsa “Verificar” para comprobarlo.
          </p>
          <div>
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
            <button class="btn btn-primary" @click="handleUpload">
              Verificar
            </button>
          </div>
        </div>
      </div>
      <div class="guxa flex justify-end">
        <img
          class="musicdibs-shadow w-full max-w-xl rounded-3xl"
          src="../assets/images/chico_guitarra.png"
          alt="Una chico tocando la guitarra"
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";

import FileFound from "../components/FileFound.vue";
import { useRegistrationsStore } from "../stores/registrations.js";

const file = ref(null);
const fileName = ref("");
const showWarning = ref(false);
const verificationResult = ref(null);

const registrationsStore = useRegistrationsStore();

onMounted(() => {
  registrationsStore.resetState();
});

watch(
  () => registrationsStore.verification,
  (newVal, oldVal) => {
    console.log("Changed from", oldVal, "to", newVal);
  },
);

const onFileChange = (event) => {
  showWarning.value = false;
  file.value = event.target.files[0];
  fileName.value = file.value.name;
};

const handleUpload = async () => {
  if (file.value === null) {
    showWarning.value = true;
    return;
  }
  try {
    verificationResult.value = await registrationsStore.verifyFile(file.value);
    console.log("Verification result:", verificationResult.value.status);
  } catch (error) {
    console.error("Error verifying file:", error);
  }
};

const handleReset = () => {
  file.value = null;
  fileName.value = "";
  showWarning.value = false;
  registrationsStore.resetState();
};
</script>

<style scoped>
.guxa {
  margin-top: -10rem;
}

.musicdibs-card {
  z-index: 10;
  position: relative;
}
</style>
