import { defineStore } from "pinia";
import api from "../api/axios.js";
import { useAuthStore } from "./auth";

export const useGenresStore = defineStore("genres", {
  state: () => ({
    genres: [],
    isLoading: false,
    error: null,
  }),

  actions: {
    // Get all genres
    async fetchAllGenres() {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.get("/genres");
        this.genres = response.data;
        return this.genres;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to fetch genres";
        console.error("Fetch genres error:", error);
      } finally {
        this.isLoading = false;
      }
    },

    // Create a new genre
    async createGenre(genreData) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.post("/genres", genreData);
        const newGenre = response.data;

        // Add to genres list if we have it loaded
        if (this.genres.length) {
          this.genres.push(newGenre);
        }

        return newGenre;
      } catch (error) {
        this.error = error.response?.data?.message || "Failed to create genre";
        console.error("Create genre error:", error);
      } finally {
        this.isLoading = false;
      }
    },

    // Delete a genre
    async deleteGenre(genreId) {
      this.isLoading = true;
      this.error = null;

      try {
        await api.delete(`/genres/${genreId}`);

        // Remove from genres list if we have it loaded
        if (this.genres.length) {
          this.genres = this.genres.filter((genre) => genre.id !== genreId);
        }

        return true;
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          `Failed to delete genre with ID: ${genreId}`;
        console.error("Delete genre error:", error);
      } finally {
        this.isLoading = false;
      }
    },

    // Reset store state
    resetState() {
      this.genres = [];
      this.isLoading = false;
      this.error = null;
    },
  },
});
