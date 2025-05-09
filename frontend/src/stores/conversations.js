import { defineStore } from "pinia";
import api from "../api/axios.js";

export const useConversationsStore = defineStore("conversations", {
  state: () => ({
    conversations: [],
    currentConversation: null,
    messages: [],
    loading: false,
    error: null,
  }),

  actions: {
    async createConversation(payload) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.post("/conversations", payload);

        this.currentConversation = response.data;
        return this.currentConversation;
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Failed to create conversation";
        console.error("Create conversation error:", error);
      } finally {
        this.loading = false;
      }
    },

    async getConversation(id) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.get(`/conversations/${id}`);
        this.currentConversation = response.data;

        return this.currentConversation;
      } catch (error) {
        this.error = error.response?.data?.detail || "Conversation not found";
        console.error("Get conversation error:", error);
      } finally {
        this.loading = false;
      }
    },

    async deleteConversation(id) {
      this.loading = true;
      this.error = null;

      try {
        await api.delete(`/conversations/${id}`);
        this.currentConversation = null;
        this.messages = [];
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Failed to delete conversation";
        console.error("Delete conversation error:", error);
      } finally {
        this.loading = false;
      }
    },

    async finishConversation(id) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.post(`/conversations/${id}/finish`);
        return response.data;
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Failed to finish conversation";
        console.error("Finishing conversation error:", error);
      } finally {
        this.loading = false;
      }
    },

    async fetchMessages(conversationId) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.get(
          `/messages/for-conversation/${conversationId}`,
        );

        this.messages = response.data;
        return this.messages;
      } catch (error) {
        this.error = error.response?.data?.detail || "Failed to load messages";
        console.error("Fetch messages error:", error);
      } finally {
        this.loading = false;
      }
    },

    async generateMessage({ conversation_id, user_message }) {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.post("/messages/generate", {
          conversation_id,
          user_message,
        });
        this.messages.push({
          content: user_message,
          is_from_ai: false,
        });
        this.messages.push(response.data);

        return this.messages;
      } catch (error) {
        this.error =
          error.response?.data?.detail || "Failed to generate message";
        console.error("Generate message error:", error);
      } finally {
        this.loading = false;
      }
    },
  },
});
