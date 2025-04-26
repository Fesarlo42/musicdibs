import { defineStore } from "pinia";
import api from "../api/axios.js";
import { useAuthStore } from "./auth";

export const useCreditsStore = defineStore("credits", {
  state: () => ({
    balance: null,
    transactionHistory: [],
    isLoading: false,
    error: null,
    pagination: {
      currentPage: 1,
      totalItems: 0,
      perPage: 10,
    },
  }),

  actions: {
    // Get user's credit balance
    async fetchBalance(userId) {
      const authStore = useAuthStore();
      if (!authStore.isLoggedIn) return null;

      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.get(`/credits/balance/${userId}`);
        this.balance = response.data;
        return this.balance;
      } catch (error) {
        this.error =
          error.response?.data?.message || "Failed to fetch credit balance";
        console.error("Fetch balance error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Add credits to user account
    async addCredits(userData) {
      const authStore = useAuthStore();
      if (!authStore.isLoggedIn) return null;

      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.post("/credits/add", userData);
        this.balance = response.data;
        return this.balance;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to add credits";
        console.error("Add credits error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Remove credits from user account
    async removeCredits(userData) {
      const authStore = useAuthStore();
      if (!authStore.isLoggedIn) return null;

      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.post("/credits/remove", userData);
        this.balance = response.data;
        return this.balance;
      } catch (error) {
        this.error =
          error.response?.data?.message || "Failed to remove credits";
        console.error("Remove credits error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Get transaction history for a user
    async fetchTransactionHistory(userId, page = 1, limit = 10) {
      const authStore = useAuthStore();
      if (!authStore.isLoggedIn) return null;

      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.get(`/credits/history/${userId}`, {
          params: {
            skip: (page - 1) * limit,
            limit,
          },
        });

        this.transactionHistory = response.data.items;
        this.pagination = {
          currentPage: page,
          totalItems: response.data.total,
          perPage: limit,
        };

        return {
          transactions: this.transactionHistory,
          pagination: this.pagination,
        };
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          "Failed to fetch transaction history";
        console.error("Fetch transaction history error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Reset store state
    resetState() {
      this.balance = null;
      this.transactionHistory = [];
      this.isLoading = false;
      this.error = null;
      this.pagination = {
        currentPage: 1,
        totalItems: 0,
        perPage: 10,
      };
    },
  },
});
