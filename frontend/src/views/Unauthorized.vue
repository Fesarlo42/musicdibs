<template>
  <div class="p-4">
    <div class="flex items-center justify-center">
      <div class="size-sm m-10">
        <img
          class="w-[90%]"
          src="../assets/images/summer_dj.png"
          alt="Not found"
        />
      </div>
      <div class="flex flex-grow-0 flex-col items-center justify-center">
        <h2 class="text-center text-4xl font-bold">
          No, tienes permiso para acceder a ese contenido.
        </h2>
        <button class="btn btn-primary btn-wide m-10">
          <router-link to="/">Volver al inicio</router-link>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup />
