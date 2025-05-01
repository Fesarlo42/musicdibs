<template>
  <div class="musicdibs-card neutral bg-base-100">
    <div class="card-body">
      <h2 class="card-title">Identidad digital</h2>
      <div v-if="error" role="alert" class="alert alert-soft alert-error">
        <span>{{ error }}</span>
      </div>
      <div class="grid grid-cols-2 gap-8">
        <div>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">ID</legend>
            <p>{{ sigData.id }}</p>
          </fieldset>
        </div>

        <div>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Estado</legend>
            <p
              class="badge badge-neutral"
              :class="{ 'badge-soft': sigData.status !== 'success' }"
            >
              {{ sigData.status || "-" }}
            </p>
          </fieldset>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  sigData: {
    type: Object,
    default: () => ({}),
  },
  error: {
    type: String,
    default: null,
  },
});
</script>
