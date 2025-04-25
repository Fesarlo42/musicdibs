import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    isAuthLoading: false,
    authError: null,
    isAuthenticated: false,
    permission: false,
  }),

  actions: {
    // Initialize store from localStorage on app start
    initializeAuth() {
      try {
        const user = JSON.parse(localStorage.getItem("user"));

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

      localStorage.setItem("user", JSON.stringify(user));
    },

    // Clear authentication data
    clearAuth() {
      this.user = null;
      this.isAuthenticated = false;

      localStorage.removeItem("user");
    },

    // Login action
    async login(credentials) {
      this.isLoading = true;
      this.error = null;

      try {
        const formData = new URLSearchParams();
        formData.append("username", credentials.email);
        formData.append("password", credentials.password);

        const response = await axios.post("/auth/login", formData, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        });

        const userData = response.data;

        this.setAuthData(userData);
        return userData;
      } catch (error) {
        this.error = error.response?.data?.message || "Login failed";
        console.error("Login error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Check if user has permission to access a specific route
    async checkPermission(requiredRole) {
      if (!this.user) return false;

      try {
        const response = await axios.get(
          `/auth/${this.user.id}/has-permission?role=${requiredRole}`,
        );

        return !!response.data.has_permission;
      } catch (error) {
        console.error("Permission check failed:", error);
        return false;
      }
    },
  },
});
