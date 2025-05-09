import { defineStore } from "pinia";
import api from "../api/axios.js";
import { useAuthStore } from "./auth";

export const useRegistrationsStore = defineStore("registrations", {
  state: () => ({
    registration: null,
    verification: null,
    isLoading: false,
    error: null,
  }),

  actions: {
    // Create a registration for a project
    async createRegistration(projectId) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.post(`/registrations/${projectId}`);
        this.registration = response.data;
        return this.registration;
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          `Failed to register project ${projectId}`;
        console.error("Registration error:", error);
      } finally {
        this.isLoading = false;
      }
    },

    // Get registration details for a project
    async getRegistration(projectId) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.get(`/registrations/${projectId}`);
        this.registration = response.data;
        return this.registration;
      } catch (error) {
        if (error.response?.status === 404) {
          return null;
        }

        this.error =
          error.response?.data?.message ||
          `Failed to get registration for project ${projectId}`;
        console.error("Get registration error:", error);
      } finally {
        this.isLoading = false;
      }
    },

    // Verify if a file is registered
    async verifyFile(file) {
      this.isLoading = true;
      this.error = null;

      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await api.post(
          "/registrations/verify-file",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          },
        );
        this.verification = response.data;
        return this.verification;
      } catch (error) {
        this.error =
          error.response?.data?.message || "File verification failed";
        console.error("File verification error:", error);
      } finally {
        this.isLoading = false;
      }
    },

    // Download registration receipt
    async downloadReceipt(receiptUrl) {
      if (!receiptUrl) {
        this.error = "No receipt URL available";
        return null;
      }

      this.isLoading = true;
      this.error = null;

      try {
        // TODO: verificar isso também
        // Open the receipt URL in a new tab or window
        window.open(receiptUrl, "_blank");
        return true;
      } catch (error) {
        this.error = "Failed to download receipt";
        console.error("Receipt download error:", error);
      } finally {
        this.isLoading = false;
      }
    },

    // Reset store state
    resetState() {
      this.registration = null;
      this.verification = null;
      this.isLoading = false;
      this.error = null;
    },
  },
});
