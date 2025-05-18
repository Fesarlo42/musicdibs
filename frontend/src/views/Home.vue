<template>
  <div class="p-0">
    <Hero />
    <section class="mt-10 px-4 pt-10">
      <h2 class="text-center font-grace text-6xl tracking-wider">
        Tu creas, nosotros protegemos
      </h2>
    </section>
    <section class="mt-11 px-4 pt-10 lg:mt-[-30px] lg:pt-0">
      <Instructions />
    </section>
    <section class="my-10 px-4 py-10">
      <div class="w-100 z-10 mx-4 p-8 glass sm:w-3/5">
        <h3 class="mb-6 text-center font-grace text-5xl/normal tracking-wider">
          Te ayudamos a proteger tus derechos de autor
        </h3>
        <p class="mb-3">
          En Musicdibs empoderamos a los creadores desde el momento de la
          creación de sus obras hasta eliminar el miedo a posibles plagios. Con
          innovadoras herramientas de inteligencia artificial y una alternativa
          a las tradicionales plataformas de registro centralizado, mediante el
          uso de las últimas tecnologías: blockchain y verificación biométrica
          de identidad
        </p>
        <p>
          Ofrecemos transparencia, seguridad y confianza, permitiendo la
          posterior verificación de registros en todo momento y desde cualquier
          parte del mundo.
        </p>
      </div>
      <div class="guxa justify-end sm:flex">
        <img
          class="musicdibs-shadow-scondary mx-4 w-full max-w-xl rounded-3xl"
          src="../assets/images/chica_cantando.png"
          alt="Una chica cantando"
        />
      </div>
    </section>
    <section class="my-10 px-4 sm:py-10">
      <h2 class="mb-7 text-center text-4xl">
        Validez legal en más de 160 países
      </h2>
      <p class="my-5">
        Cada registro en Musicdibs genera un certificado digital inmutable y
        verificable que sirve como prueba legal de autoría. Si alguna vez
        necesitas defender tu creación en un conflicto legal, tu certificación
        Musicdibs te respalda ya que cumplimos con las siguientes normativas:
      </p>
      <div class="mt-10 grid gap-8 sm:grid-cols-1 md:grid-cols-2">
        <div class="flex items-center gap-4">
          <div class="rounded-full bg-primary p-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="size-10 fill-primary-content"
            >
              <path
                fill-rule="evenodd"
                d="M12.516 2.17a.75.75 0 0 0-1.032 0 11.209 11.209 0 0 1-7.877 3.08.75.75 0 0 0-.722.515A12.74 12.74 0 0 0 2.25 9.75c0 5.942 4.064 10.933 9.563 12.348a.749.749 0 0 0 .374 0c5.499-1.415 9.563-6.406 9.563-12.348 0-1.39-.223-2.73-.635-3.985a.75.75 0 0 0-.722-.516l-.143.001c-2.996 0-5.717-1.17-7.734-3.08Zm3.094 8.016a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <span class="text-lg">
            <a
              class="btn-link"
              href="https://www.wipo.int/treaties/es/ip/berne/"
              target="_blank"
              >Convenio de Berna</a
            >
            para la protección de obras literarias y artísticas.</span
          >
        </div>

        <div class="flex items-center gap-4">
          <div class="rounded-full bg-primary p-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="size-10 fill-primary-content"
            >
              <path
                fill-rule="evenodd"
                d="M12.516 2.17a.75.75 0 0 0-1.032 0 11.209 11.209 0 0 1-7.877 3.08.75.75 0 0 0-.722.515A12.74 12.74 0 0 0 2.25 9.75c0 5.942 4.064 10.933 9.563 12.348a.749.749 0 0 0 .374 0c5.499-1.415 9.563-6.406 9.563-12.348 0-1.39-.223-2.73-.635-3.985a.75.75 0 0 0-.722-.516l-.143.001c-2.996 0-5.717-1.17-7.734-3.08Zm3.094 8.016a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <span class="text-lg">
            <a
              class="btn-link"
              href="https://www.wipo.int/treaties/es/ip/wct/"
              target="_blank"
              >Tratado de la OMPI</a
            >
            sobre derecho de autor.</span
          >
        </div>

        <div class="flex items-center gap-4">
          <div class="rounded-full bg-primary p-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="size-10 fill-primary-content"
            >
              <path
                fill-rule="evenodd"
                d="M12.516 2.17a.75.75 0 0 0-1.032 0 11.209 11.209 0 0 1-7.877 3.08.75.75 0 0 0-.722.515A12.74 12.74 0 0 0 2.25 9.75c0 5.942 4.064 10.933 9.563 12.348a.749.749 0 0 0 .374 0c5.499-1.415 9.563-6.406 9.563-12.348 0-1.39-.223-2.73-.635-3.985a.75.75 0 0 0-.722-.516l-.143.001c-2.996 0-5.717-1.17-7.734-3.08Zm3.094 8.016a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <span class="text-lg">
            <a
              class="btn-link"
              href="https://digital-strategy.ec.europa.eu/es/policies/copyright"
              target="_blank"
            >
              Directiva Europea sobre Derechos de Autor en la Era Digital.</a
            ></span
          >
        </div>

        <div class="flex items-center gap-4">
          <div class="rounded-full bg-primary p-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="size-10 fill-primary-content"
            >
              <path
                fill-rule="evenodd"
                d="M12.516 2.17a.75.75 0 0 0-1.032 0 11.209 11.209 0 0 1-7.877 3.08.75.75 0 0 0-.722.515A12.74 12.74 0 0 0 2.25 9.75c0 5.942 4.064 10.933 9.563 12.348a.749.749 0 0 0 .374 0c5.499-1.415 9.563-6.406 9.563-12.348 0-1.39-.223-2.73-.635-3.985a.75.75 0 0 0-.722-.516l-.143.001c-2.996 0-5.717-1.17-7.734-3.08Zm3.094 8.016a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <span class="text-lg">
            <a
              class="btn-link"
              href="https://www.legalondo.com/regulacion-del-uso-de-tecnologia-blockchain-en-la-propiedad-intelectual/"
              target="_blank"
              >Regulaciones Blockchain</a
            >
            aplicadas a la Propiedad Intelectual</span
          >
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useAuthStore } from "../stores/auth.js";

import Hero from "../components/Hero.vue";
import Instructions from "../components/Instructions.vue";

const authStore = useAuthStore();

onMounted(() => {
  authStore.initializeAuth();
});
</script>

<style scoped>
.guxa {
  margin-top: -20rem;
}
</style>
