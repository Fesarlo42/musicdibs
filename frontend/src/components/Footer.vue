<template>
  <footer>
    <section class="pt-[150px]">
      <h2 class="font-grace text-center text-7xl tracking-wider">
        Empieza ahora gratis
      </h2>
      <div class="flex justify-center">
        <router-link to="/signup">
          <button class="btn btn-primary btn-lg btn-wide my-5">
            Proteger mi obra
          </button>
        </router-link>
      </div>
    </section>
    <div
      class="footer mx-auto block max-w-full p-10 text-base-content sm:footer-horizontal sm:max-w-screen-lg"
    >
      <div class="p-5">
        <router-link to="/">
          <img
            class="w-24"
            src="../assets/images/logo_dark@2x.png"
            alt="Musicdibs Logo"
          />
        </router-link>
      </div>
      <div class="w-full justify-between p-5 sm:flex">
        <nav>
          <ul class="menu menu-horizontal p-0 text-base">
            <li><router-link to="/verify">Verificar obra</router-link></li>
            <li><router-link to="/dashboard">Dashboard</router-link></li>
            <li><router-link to="/dashboard_admin">Dashboard</router-link></li>
            <li><router-link to="/projects">Mis poryectos</router-link></li>
            <li><router-link to="/new_project">Nuevo poryecto</router-link></li>
            <li><router-link to="/settings">Ajustes</router-link></li>
            <li><router-link to="/login">Acceder</router-link></li>
            <li><router-link to="/signup">Registrarse</router-link></li>
            <li><router-link to="/logout">Salir</router-link></li>
          </ul>
        </nav>
        <nav>
          <div class="grid grid-flow-col gap-4 p-3">
            <a href="https://www.instagram.com/musicdibs/" target="_blank">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="lucide lucide-instagram-icon lucide-instagram hover:primary"
              >
                <rect width="20" height="20" x="2" y="2" rx="5" ry="5" />
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
                <line x1="17.5" x2="17.51" y1="6.5" y2="6.5" />
              </svg>
            </a>
            <a href="https://x.com/musicdibs" target="_blank">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                class="fill-current"
              >
                <path
                  d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"
                ></path>
              </svg>
            </a>
            <a href="https://www.youtube.com/@Musicdibs" target="_blank">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                class="fill-current"
              >
                <path
                  d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"
                ></path>
              </svg>
            </a>
          </div>
        </nav>
      </div>
    </div>
    <div class="bg-neutral p-3 text-center text-sm font-light">
      <p class="mx-auto max-w-screen-lg px-4">
        Proyecto realizado por Fernanda Gomes en el marco del módulo de Proyecto
        Final de Ciclo en el curso de Formación Profesional en Desarrollo de
        Aplicaciones Web
      </p>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<style scoped>
footer {
  background-image: url(/src/assets/images/bg_music.png);
  background-size: 65%;
  background-position: center center;
  background-repeat: repeat-x;
}

a > svg:hover {
  @apply transition-colors;
  fill: var(--color-primary);
}

@media (max-width: 800px) {
  footer {
    background-size: cover;
  }
}
</style>
