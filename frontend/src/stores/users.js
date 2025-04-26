import { defineStore } from "pinia";
import api from "../api/axios.js";

export const useUsersStore = defineStore("users", {
  state: () => ({
    users: [],
    user: null,
    isLoading: false,
    error: null,
  }),

  actions: {
    // Get all users
    async fetchUsers() {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.get("/users");
        this.users = response.data;
        return this.users;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to fetch users";
        console.error("Fetch users error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Get single user
    async fetchUser(userId) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.get(`/users/${userId}`);
        this.user = response.data;
        return this.user;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to fetch user";
        console.error("Fetch user error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Register new user
    async createUser(userData) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.post("/users", userData);
        const newUser = response.data;

        // Add to users list if we're maintaining it
        if (this.users.length) {
          this.users.push(newUser);
        }

        return newUser;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to create user";
        console.error("Create user error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Update user data
    async updateUser(userId, userData) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.put(`/users/${userId}`, userData);
        const updatedUser = response.data;

        // Update in the users list if it exists
        if (this.users.length) {
          const index = this.users.findIndex((user) => user.id === userId);
          if (index !== -1) {
            this.users[index] = updatedUser;
          }
        }

        // Update current user if it's the same
        if (this.user && this.user.id === userId) {
          this.user = updatedUser;
        }

        return updatedUser;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to update user";
        console.error("Update user error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Delete user
    async deleteUser(userId) {
      this.isLoading = true;
      this.error = null;

      try {
        await api.delete(`/users/${userId}`);

        // Remove from users list if it exists
        if (this.users.length) {
          this.users = this.users.filter((user) => user.id !== userId);
        }

        // Clear current user if it's the same
        if (this.user && this.user.id === userId) {
          this.user = null;
        }

        return true;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to delete user";
        console.error("Delete user error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Sign user (for signature endpoint)
    async makeSignature(userId) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.post(`/users/${userId}/signature`);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to sign user";
        console.error("Sign user error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
  },
});
