<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Acceder</h1>
    <section class="my-10 py-10">
      <div class="musicdibs-card secondary w-full bg-base-100 sm:w-3/5">
        <div class="card-body">
          <h2 class="card-title">Acceder</h2>
          <p>
            Rellena el formuliario para acceder a tu cuenta de Musicdibs. Si no
            tienes cuenta, puedes crearla de forma gratuita.
          </p>
          <div>
            <div
              v-if="authStore.error"
              role="alert"
              class="alert alert-soft alert-error"
            >
              <span>{{ authStore.error }}</span>
            </div>
            <fieldset class="fieldset">
              <legend class="fieldset-legend">Correo electrónico</legend>
              <input
                class="validator input"
                type="email"
                required
                placeholder="mail@site.com"
                v-model="email"
              />
              <div class="validator-hint hidden">
                Introduzca una dirección de correo electrónico válida
              </div>
            </fieldset>
            <fieldset class="fieldset relative">
              <legend class="fieldset-legend">Contraseña</legend>
              <input
                class="validator input"
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                minlength="8"
                required
                placeholder="********"
              />
              <div
                class="absolute right-3 top-[25px] z-10 -translate-y-1/2 cursor-pointer opacity-60"
                @click="togglePassword"
              >
                <svg
                  v-if="showPassword"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="size-6"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
                  />
                </svg>

                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="size-6"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                  />
                </svg>
              </div>
              <div class="validator-hint">
                La contraseña es obligatoria y debe tener al menos 8 caracteres.
              </div>
            </fieldset>
            <div class="mt-3 flex gap-4">
              <button class="btn btn-secondary" @click="handleLogin">
                <span
                  v-if="authStore.isLoading"
                  class="loading loading-dots loading-md"
                ></span>
                <span v-else>Acceder</span>
              </button>
              <button class="btn btn-secondary btn-outline">
                <router-link to="/signup">Crear cuenta</router-link>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="guxa flex justify-end">
        <img
          class="musicdibs-shadow-scondary max-w-xl rounded-3xl"
          src="../assets/images/chico_producer.png"
          alt="Una chico tocando la guitarra"
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth.js";

const email = ref("");
const password = ref("");
const showPassword = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

// Validators
const isValidEmail = computed(() =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value),
);

const isValidPassword = computed(() => password.value.length >= 8);

const handleLogin = async () => {
  if (!isValidEmail.value || !isValidPassword.value) {
    alert("Por favor, revise los campos antes de continuar.");
    return;
  }

  try {
    await authStore.login({
      username: email.value,
      password: password.value,
    });

    const isAdmin = await authStore.checkPermission("admin");
    if (isAdmin) {
      return router.push("/dashboard_admin");
    }

    return router.push("/dashboard");
  } catch (error) {
    console.error("Error loging in:", error);
  }

  email.value = "";
  password.value = "";
};
</script>

<style scoped>
.guxa {
  margin-top: -15rem;
}
.musicdibs-card {
  z-index: 10;
  position: relative;
}
</style>
