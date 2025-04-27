import { computed, ref, onMounted } from "vue";
import { useAuthStore } from "../stores/auth.js";

export function useAuthStatus() {
  const authStore = useAuthStore();

  authStore.initializeAuth();

  const isLoggedIn = computed(() => authStore.isAuthenticated);
  const isAdmin = ref(false);

  const checkAdmin = async () => {
    try {
      isAdmin.value = await authStore.checkPermission("admin");
    } catch (error) {
      console.error("Error checking admin permission:", error);
      isAdmin.value = false;
    }
  };

  onMounted(() => {
    if (isLoggedIn.value) {
      checkAdmin();
    }
  });

  return { isLoggedIn, isAdmin, checkAdmin };
}
