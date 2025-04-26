import { defineStore } from "pinia";
import api from "../api/axios.js";
import { useAuthStore } from "./auth";

export const useProjectsStore = defineStore("projects", {
  state: () => ({
    projects: [],
    currentProject: null,
    projectFiles: [],
    isLoading: false,
    error: null,
    pagination: {
      currentPage: 1,
      totalPages: 1,
      totalItems: 0,
      perPage: 10,
    },
    filters: {
      searchQuery: "",
      sortBy: "createdAt",
      sortOrder: "desc",
    },
  }),

  actions: {
    // Get all user projects with optional filtering and pagination
    async fetchProjects(params = {}) {
      this.isLoading = true;
      this.error = null;

      try {
        // Merge default filters with provided params
        const queryParams = {
          page: params.page || this.pagination.currentPage,
          limit: params.limit || this.pagination.perPage,
          search: params.search || this.filters.searchQuery,
          sortBy: params.sortBy || this.filters.sortBy,
          sortOrder: params.sortOrder || this.filters.sortOrder,
        };

        const response = await api.get(`users/${params.user_id}/projects`, {
          params: queryParams,
        });

        this.projects = response.data.projects;

        // Update pagination info
        this.pagination = {
          currentPage: response.data.pagination.currentPage,
          totalPages: response.data.pagination.totalPages,
          totalItems: response.data.pagination.totalItems,
          perPage: response.data.pagination.perPage,
        };

        // Update filters if they were changed
        if (params.page) this.filters.currentPage = params.page;
        if (params.search) this.filters.searchQuery = params.search;
        if (params.sortBy) this.filters.sortBy = params.sortBy;
        if (params.sortOrder) this.filters.sortOrder = params.sortOrder;

        return this.projects;
      } catch (error) {
        this.error =
          error.response?.data?.message || "Failed to fetch projects";
        console.error("Fetch projects error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Get a specific project by ID
    async fetchProjectById(id) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.get(`/projects/${id}`);
        this.currentProject = response.data;

        // Also update in the projects array if it exists there
        const projectIndex = this.projects.findIndex((p) => p.id === id);
        if (projectIndex !== -1) {
          this.projects[projectIndex] = response.data;
        }

        return this.currentProject;
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          `Failed to fetch project with ID: ${id}`;
        console.error("Fetch project error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Create a new project
    async createProject(projectData) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.post("/projects", projectData);
        const newProject = response.data;

        // Add the new project to the array and make it current
        this.projects.unshift(newProject);
        this.currentProject = newProject;

        // Increment total count in pagination
        this.pagination.totalItems++;

        return newProject;
      } catch (error) {
        this.error =
          error.response?.data?.message || "Failed to create project";
        console.error("Create project error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Update an existing project
    async updateProject(id, projectData) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.put(`/projects/${id}`, projectData);
        const updatedProject = response.data;

        // Update in the projects array
        const projectIndex = this.projects.findIndex((p) => p.id === id);
        if (projectIndex !== -1) {
          this.projects[projectIndex] = updatedProject;
        }

        // Update current project if it's the one being edited
        if (this.currentProject && this.currentProject.id === id) {
          this.currentProject = updatedProject;
        }

        return updatedProject;
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          `Failed to update project with ID: ${id}`;
        console.error("Update project error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Delete a project
    async deleteProject(id) {
      this.isLoading = true;
      this.error = null;

      try {
        await api.delete(`/projects/${id}`);

        // Remove from the projects array
        this.projects = this.projects.filter((p) => p.id !== id);

        // Clear current project if it's the one being deleted
        if (this.currentProject && this.currentProject.id === id) {
          this.currentProject = null;
        }

        // Decrement total count in pagination
        this.pagination.totalItems--;

        return true;
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          `Failed to delete project with ID: ${id}`;
        console.error("Delete project error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Add a genre to a project
    async addGenreToProject(projectId, genreId) {
      this.isLoading = true;
      this.error = null;

      try {
        await api.post(`/projects/${projectId}/genres/${genreId}`);

        // Refresh project data to get updated genres
        await this.fetchProjectById(projectId);

        return true;
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          `Failed to add genre ${genreId} to project ${projectId}`;
        console.error("Add genre to project error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Remove a genre from a project
    async removeGenreFromProject(projectId, genreId) {
      this.isLoading = true;
      this.error = null;

      try {
        await api.delete(`/projects/${projectId}/genres/${genreId}`);

        // Refresh project data to get updated genres
        await this.fetchProjectById(projectId);

        return true;
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          `Failed to remove genre ${genreId} from project ${projectId}`;
        console.error("Remove genre from project error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Upload a file to a project
    async uploadProjectFile(projectId, file) {
      this.isLoading = true;
      this.error = null;

      try {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append("file", file);

        const response = await api.post(`/files/${projectId}`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        const newFile = response.data;

        // If we have project files loaded, add this one to the array
        if (this.projectFiles.length > 0) {
          this.projectFiles.push(newFile);
        }

        return newFile;
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          `Failed to upload file to project ${projectId}`;
        console.error("Upload file error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Delete a project file
    async deleteProjectFile(fileId) {
      this.isLoading = true;
      this.error = null;

      try {
        await api.delete(`/files/${fileId}`);

        // Remove file from local state if it exists
        this.projectFiles = this.projectFiles.filter(
          (file) => file.id !== fileId,
        );

        return true;
      } catch (error) {
        this.error =
          error.response?.data?.message || `Failed to delete file ${fileId}`;
        console.error("Delete file error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Get download URL for a file
    async downloadFile(fileId) {
      this.isLoading = true;
      this.error = null;

      try {
        // TODO: revisar eso!!
        // This would typically open in a new tab or trigger a download
        // We'll return the URL that the component can use
        const url = `/files/${fileId}/download`;

        // We can either return the URL for the component to handle
        // or directly trigger the download with window.open

        // Option 1: Return URL for component to handle
        return url;

        // Option 2: Directly trigger download
        // window.open(url, '_blank');
        // return true;
      } catch (error) {
        this.error =
          error.response?.data?.message || `Failed to download file ${fileId}`;
        console.error("Download file error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Get all files for a project
    async fetchProjectFiles(projectId) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.get(`/files/project/${projectId}`);
        this.projectFiles = response.data;
        return this.projectFiles;
      } catch (error) {
        this.error =
          error.response?.data?.message ||
          `Failed to fetch files for project ${projectId}`;
        console.error("Fetch project files error:", error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // Reset store state
    resetState() {
      this.projects = [];
      this.currentProject = null;
      this.projectFiles = [];
      this.isLoading = false;
      this.error = null;
      this.pagination = {
        currentPage: 1,
        totalPages: 1,
        totalItems: 0,
        perPage: 10,
      };
      this.filters = {
        searchQuery: "",
        sortBy: "createdAt",
        sortOrder: "desc",
      };
    },
  },
});
