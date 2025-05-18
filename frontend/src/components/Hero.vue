<template>
  <div class="-mx-[calc((100vw-100%)/2)] w-screen shadow-lg">
    <div class="relative min-h-screen overflow-hidden">
      <div class="isolate">
        <!-- Background Image (fallback for when video fails to load or before it does) -->
        <img
          src="../assets/images/dj_bg.jpg"
          alt="Musicidbs hero image"
          class="absolute inset-0 h-full w-full object-cover"
        />

        <!-- Background Video -->
        <video
          autoplay
          muted
          loop
          playsinline
          class="absolute inset-0 h-full w-full object-cover"
        >
          <source
            src="../assets/videos/Pieza_web_musicdibs.mp4"
            type="video/mp4"
          />
        </video>

        <!-- Overlay -->
        <div
          class="absolute inset-0 bg-base-300 bg-opacity-10 mix-blend-lighten"
        ></div>
      </div>
      <!-- Content -->
      <div
        class="relative z-10 flex min-h-screen items-center justify-center text-center text-neutral-content"
      >
        <div class="max-w-4xl px-8 text-white">
          <h1 class="my-9 font-grace text-8xl tracking-wider">
            Tu musica, siempre tuya
          </h1>
          <h2 class="mb-5 text-pretty text-2xl/9">
            Protege tus creaciones de la forma más segura e innovadora gracias a
            la tecnología blockchain.
          </h2>
          <router-link to="/signup"
            ><button class="btn btn-primary btn-lg btn-wide my-5">
              Empezar ya
            </button></router-link
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script setup />
