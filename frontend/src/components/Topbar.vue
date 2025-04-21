<template>
  <div class="fixed left-0 right-0 top-0 z-20 h-20 bg-neutral p-2 shadow-md">
    <div class="mx-auto max-w-screen-lg sm:flex">
      <div class="navbar-start">
        <div class="dropdown">
          <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h8m-8 6h16"
              />
            </svg>
          </div>
          <ul
            tabindex="0"
            class="z-1 dropdown-content menu menu-sm mt-3 w-52 rounded-box bg-base-100 p-2 text-base shadow"
          >
            <li><router-link to="/verify">Verificar obra</router-link></li>
            <li><router-link to="/dashboard">Dashboard</router-link></li>
            <li><router-link to="/dashboard_admin">Dashboard</router-link></li>
            <li><router-link to="/projects">Mis poryectos</router-link></li>
            <li><router-link to="/settings">Ajustes</router-link></li>
            <li><router-link to="/logout">Salir</router-link></li>
          </ul>
        </div>
        <router-link to="/">
          <img
            class="logo block"
            src="../assets/images/logo_dark@2x.png"
            alt="Musicdibs Logo"
          />
        </router-link>
      </div>
      <div class="navbar-center hidden lg:flex">
        <ul class="menu menu-horizontal px-1">
          <li><router-link to="/verify">Verificar obra</router-link></li>
          <li><router-link to="/dashboard">Dashboard</router-link></li>
          <li><router-link to="/dashboard_admin">Dashboard</router-link></li>
          <li><router-link to="/projects">Mis poryectos</router-link></li>
          <li><router-link to="/settings">Ajustes</router-link></li>
          <li><router-link to="/logout">Salir</router-link></li>
        </ul>
      </div>
      <div class="navbar-end">
        <ul class="menu menu-horizontal px-1">
          <li>
            <router-link to="/new_project">
              <button class="btn btn-primary border-0">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  class="size-5"
                >
                  <path
                    fill-rule="evenodd"
                    d="M12 3.75a.75.75 0 0 1 .75.75v6.75h6.75a.75.75 0 0 1 0 1.5h-6.75v6.75a.75.75 0 0 1-1.5 0v-6.75H4.5a.75.75 0 0 1 0-1.5h6.75V4.5a.75.75 0 0 1 .75-.75Z"
                    clip-rule="evenodd"
                  />
                </svg>
                Nuevo proyecto
              </button>
            </router-link>
          </li>
          <li><router-link to="/login">Acceder</router-link></li>
          <li>
            <router-link to="/signup">
              <button class="btn btn-primary border-0">Registrarse</button>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TopBar",
};
</script>
