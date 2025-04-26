<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Registro</h1>
    <section class="my-10 py-10">
      <div class="musicdibs-card secondary w-full bg-base-100 sm:w-3/5">
        <div class="card-body">
          <h2 class="card-title">Crear cuenta</h2>
          <p>
            Rellena el formulario para crear tu cuenta en Musicdibs y comenzar a
            proteger tus obras.
          </p>

          <div
            v-if="usersStore.error"
            role="alert"
            class="alert alert-soft alert-error"
          >
            <span>{{ usersStore.error }}</span>
          </div>
          <div
            v-if="validationError"
            role="alert"
            class="alert alert-soft alert-error"
          >
            <span>{{ validationError }}</span>
          </div>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Nombre</legend>
            <input
              class="validator input"
              type="text"
              v-model="firstName"
              required
              placeholder="Tu nombre"
            />
            <div class="validator-hint hidden">
              El nombre no puede estar vacío
            </div>
          </fieldset>

          <fieldset class="fieldset">
            <legend class="fieldset-legend">Apellido</legend>
            <input
              class="validator input"
              type="text"
              v-model="lastName"
              required
              placeholder="Tu apellido"
            />
            <div class="validator-hint hidden">
              El apellido no puede estar vacío
            </div>
          </fieldset>

          <fieldset class="fieldset">
            <legend class="fieldset-legend">Correo electrónico</legend>
            <input
              class="validator input"
              type="email"
              v-model="email"
              required
              placeholder="mail@site.com"
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
              required
              minlength="8"
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
            <div class="validator-hint hidden">
              La contraseña es obligatoria y debe tener al menos 8 caracteres.
            </div>
          </fieldset>

          <!-- Confirm Password -->
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Confirmar contraseña</legend>
            <input
              class="validator input"
              :type="showPassword ? 'text' : 'password'"
              v-model="confirmPassword"
              required
              minlength="8"
              placeholder="********"
            />
            <div class="validator-hint">Las contraseñas no coinciden.</div>
          </fieldset>

          <div class="mt-3 flex gap-4">
            <button class="btn btn-secondary" @click="handleSignup">
              <span
                v-if="usersStore.isLoading"
                class="loading loading-dots loading-md"
              ></span>
              <span v-else>Crear cuenta</span>
            </button>
            <button class="btn btn-secondary btn-outline">
              <router-link to="/login">¿Ya tienes cuenta?</router-link>
            </button>
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

import { useUsersStore } from "../stores/users.js";
import { useAuthStore } from "../stores/auth.js";
import { useCreditsStore } from "../stores/credits.js";

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const firstName = ref("");
const lastName = ref("");
const showPassword = ref(false);
const validationError = ref(false);

const usersStore = useUsersStore();
const authStore = useAuthStore();
const creditsStore = useCreditsStore();
const router = useRouter();

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

// Validators
const isValidEmail = computed(() =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value),
);

const isValidPassword = computed(() => password.value.length >= 8);

const passwordsMatch = computed(() => password.value === confirmPassword.value);

const validateSignup = () => {
  if (firstName.value.length < 1) {
    validationError.value = "El nombre no puede estar vacío.";
    return false;
  }
  if (lastName.value.length < 1) {
    validationError.value = "El apellido no puede estar vacío.";
    return false;
  }
  if (!isValidEmail.value) {
    validationError.value = "El correo electrónico no es valido.";
    return false;
  }
  if (!isValidPassword.value) {
    validationError.value =
      "La contraseña es obligatoria y debe tener al menos 8 caracteres.";
    return false;
  }

  if (!passwordsMatch.value) {
    validationError.value = "Las contraseñas no coinciden.";
    return false;
  }

  return true;
};

const handleSignup = async () => {
  if (!validateSignup()) {
    return;
  }

  try {
    const userData = await usersStore.createUser({
      email: email.value,
      password: password.value,
      first_name: firstName.value,
      last_name: lastName.value,
      role: "user",
    });

    // Gie user 5 credits after signup
    await creditsStore.addCredits(userData.id, 5);

    // login user after signup
    await authStore.login({
      username: email.value,
      password: password.value,
    });

    router.push("/dashboard");
  } catch (error) {
    console.error("Error creating account:", error);
  }

  email.value = "";
  password.value = "";
  confirmPassword.value = "";
  firstName.value = "";
  lastName.value = "";
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
