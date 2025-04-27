import { defineStore } from "pinia";
import api from "../api/axios.js";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    isLoading: false,
    error: null,
    isAuthenticated: false,
    permission: false,
  }),

  actions: {
    // Initialize store from sessionStorage on app start
    initializeAuth() {
      try {
        const rawUser = sessionStorage.getItem("user");
        const user = JSON.parse(rawUser);
        if (user) {
          this.setAuthData(user);
        }
      } catch (error) {
        this.clearAuth();
        console.error("Failed to initialize auth from storage:", error);
      }
    },

    setAuthData(user) {
      this.user = user;
      this.isAuthenticated = true;
      this.error = null;

      sessionStorage.setItem("user", JSON.stringify(user));
    },

    // Clear authentication data
    clearAuth() {
      this.user = null;
      this.isAuthenticated = false;

      sessionStorage.removeItem("user");
    },

    // Login action
    async login(credentials) {
      this.isLoading = true;
      this.error = null;

      try {
        const formData = new URLSearchParams();
        formData.append("username", credentials.username);
        formData.append("password", credentials.password);

        const response = await api.post("/auth/login", formData, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        });

        const userData = response.data;

        this.setAuthData(userData);
        return userData;
      } catch (error) {
        if (error.response?.status === 401) {
          this.error = "Correo electrónico o contraseña incorrectos";
        } else {
          this.error =
            `${error.response?.status} ${error.response?.data?.message}` ||
            "Login failed";
        }
        console.error("Login error:", error);
      } finally {
        this.isLoading = false;
      }
    },

    // Check if user has permission to access a specific route
    async checkPermission(requiredRole) {
      if (!this.user) return false;

      try {
        const response = await api.get(
          `/auth/${this.user.id}/has-permission?role=${requiredRole}`,
        );

        this.permission = !!response.data.has_permission;
        return this.permission;
      } catch (error) {
        console.error("Permission check failed:", error);
        return false;
      }
    },
  },
});
