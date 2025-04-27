<template>
  <dialog id="ibs_sig_modal" class="modal modal-bottom sm:modal-middle">
    <div class="musicdisbs-card modal-box bg-base-100">
      <div class="card-body p-0 text-base-200">
        <h2 class="card-title">Bienvenido a Musicdibs</h2>
        <p v-if="sigStatus == 'not_found'">
          Para empezar a usar la plataforma, necesitas crear una identidad
          digital con la que registrarás tus proyectos en blockchain. Pincha en
          el botón abajo para empezar el proceso.
        </p>
        <p v-else-if="sigStatus == 'created'">
          Has empezado el proceso de crear tu identidad digital, pero por alguna
          razón lo has dejado sin completar. Pincha en el botón abajo para
          volver a empezar el proceso.
        </p>
        <p v-else-if="sigStatus == 'failed'">
          El proceso de creación de tu identidad digital ha fallado. Pincha en
          el botón abajo para volver a empezarlo.
        </p>
      </div>
      <div class="modal-action">
        <button
          class="btn btn-primary btn-block mt-4 border-0"
          @click="handleKyc"
        >
          Verificar identidad
        </button>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { onMounted, ref } from "vue";

import { useUsersStore } from "../stores/users.js";
import { useAuthStore } from "../stores/auth.js";

const authStore = useAuthStore();
const usersStore = useUsersStore();

const sigStatus = ref("");

onMounted(async () => {
  const hasKyc = await usersStore.getSignatureInfo(authStore.user.id);
  console.log("hasKyc", hasKyc);

  sigStatus.value = hasKyc.status;

  if (
    hasKyc.status == "not_found" ||
    hasKyc.status == "created" ||
    hasKyc.status == "failed"
  ) {
    const modal = document.getElementById("ibs_sig_modal");
    modal.showModal();
  }
});

const handleKyc = async () => {
  const kycData = await usersStore.makeSignature(authStore.user.id);
  window.open(kycData.url, "_blank");
};
</script>
