<template>
  <div class="musicdibs-card secondary bg-base-100">
    <div class="card-body">
      <h2 class="card-title">Historial de creditos</h2>
      <div v-if="error" role="alert" class="alert alert-soft alert-error">
        <span>{{ error }}</span>
      </div>
      <p>Total de creditos: {{ balance }}</p>
      <div class="overflow-x-auto">
        <table class="table">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Cantidad</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="transaction in transactionHistory" :key="transaction.id">
              <td>{{ formatDate(transaction.transaction_date) }}</td>
              <td>{{ transaction.amount }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  balance: {
    type: Number,
  },
  transactionHistory: {
    type: Array,
  },
  error: {
    type: String,
    default: null,
  },
});

const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};
</script>
