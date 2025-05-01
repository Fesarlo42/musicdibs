<template>
  <dialog id="credits_modal" class="modal modal-bottom sm:modal-middle">
    <div class="musicdibs-card modal-box bg-base-100">
      <form method="dialog">
        <button
          class="btn btn-ghost btn-sm btn-circle absolute right-2 top-2 text-primary-content"
        >
          ✕
        </button>
      </form>
      <div class="card-body space-y-4 p-0 text-base-200">
        <h2 class="card-title">Gestionar créditos</h2>
        <div
          v-if="creditsStore.error"
          role="alert"
          class="alert alert-soft alert-error"
        >
          <span>{{ creditsStore.error }}</span>
        </div>
        <p>
          Ajusta el saldo de créditos.
          <br />
          Para <strong>añadir</strong> créditos, introduce un número positivo.
          Para <strong>restar</strong> créditos, introduce un número negativo.
        </p>

        <input
          v-model.number="creditInput"
          type="number"
          class="input-bordered input w-full"
          placeholder="Introduce la cantidad de créditos"
        />

        <button
          class="btn btn-primary w-full"
          :disabled="creditsStore.isLoading || creditInput === 0"
          @click="handleAdjustCredits"
        >
          <span
            v-if="creditsStore.isLoading"
            class="loading loading-dots loading-md"
          ></span>
          <span v-else>Actualizar créditos</span>
        </button>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { ref } from "vue";
import { useCreditsStore } from "../stores/credits.js";

const creditsStore = useCreditsStore();

const props = defineProps({
  userId: {
    type: Number,
    required: true,
  },
  balance: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["balance-updated"]);

const creditInput = ref(0);

const handleAdjustCredits = async () => {
  if (creditInput.value === 0) return;

  if (creditInput.value > 0) {
    await creditsStore.addCredits(props.userId, creditInput.value);
  } else {
    await creditsStore.removeCredits(props.userId, Math.abs(creditInput.value));
  }

  if (creditsStore.error) {
    return;
  }

  creditInput.value = 0;
  const modal = document.getElementById("credits_modal");
  emit("balance-updated");
  modal?.close?.();
};
</script>
