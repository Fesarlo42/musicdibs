import { createRouter, createWebHistory } from "vue-router";

// views
import Home from "../views/Home.vue";
import Verify from "../views/Verify.vue";
import Signup from "../views/Signup.vue";
import Login from "../views/Login.vue";
import Unauthorized from "../views/Unauthorized.vue";
import NotFound from "../views/NotFound.vue";

import DashboardUser from "../views/DashboardUser.vue";
import ProjectList from "../views/ProjectList.vue";
import ProjectDetails from "../views/ProjectDetails.vue";
import ProjectNew from "../views/ProjectNew.vue";

import DashboardAdmin from "../views/DashboardAdmin.vue";
import ManageUser from "../views/ManageUser.vue";

import Settings from "../views/Settings.vue";
import Logout from "../views/Logout.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { title: "Musicdibs" },
  },
  {
    path: "/verify",
    name: "Verify",
    component: Verify,
    meta: { title: "Verificar obra - Musicdibs" },
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
    meta: { title: "Registrarse - Musicdibs" },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { title: "Acceder - Musicdibs" },
  },

  {
    path: "/dashboard",
    name: "DashboardUser",
    component: DashboardUser,
    meta: { title: "Dashboard - Musicdibs" },
  },
  {
    path: "/projects/:ref",
    name: "ProjectDetails",
    component: ProjectDetails,
    meta: { title: "Proyecto - Musicdibs" },
  },
  {
    path: "/projects",
    name: "ProjectList",
    component: ProjectList,
    meta: { title: "Mis proyectos - Musicdibs" },
  },
  {
    path: "/new_project",
    name: "ProjectNew",
    component: ProjectNew,
    meta: { title: "Nuevo proyecto - Musicdibs" },
  },

  {
    path: "/dashboard_admin",
    name: "DashboardAdmin",
    component: DashboardAdmin,
    meta: { title: "Dashboard de administración - Musicdibs" },
  },
  {
    path: "/manage_users",
    name: "ManageUser",
    component: ManageUser,
    meta: { title: "Gestionar usuario - Musicdibs" },
  },

  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: { title: "Ajustes - Musicdibs" },
  },
  {
    path: "/logout",
    name: "Logout",
    component: Logout,
    meta: { title: "Salir - Musicdibs" },
  },

  {
    path: "/unauthorized",
    name: "Unauthorized",
    component: Unauthorized,
    meta: { title: "No autorizado - Musicdibs" },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
    meta: { title: "No encontrado - Musicdibs" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

// access control
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "Musicdibs";

  const userData = JSON.parse(sessionStorage.getItem("user"));
  const userRole = userData?.role;

  const protectedRoutes = [
    "/dashboard",
    "/projects",
    "/new_project",
    "/settings",
  ];
  const adminRoutes = ["/dashboard_admin", "/manage_users"];

  if (adminRoutes.includes(to.path)) {
    if (!userData) {
      return next("/login");
    }

    if (userRole !== "admin") {
      return next("/unauthorized");
    }
  }

  if (protectedRoutes.includes(to.path)) {
    if (!userData) {
      return next("/login");
    }
  }

  if ((to.path === "/login" || to.path === "/signup") && userData) {
    if (userRole == "admin") {
      return next("/dashboard_admin");
    }
    return next("/dashboard");
  }

  next();
});

export default router;
