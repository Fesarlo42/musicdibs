// stores/index.js
import { createPinia } from "pinia";
import { markRaw } from "vue";
import router from "../router";

// Create Pinia instance
const pinia = createPinia();

// Add router to Pinia as a plugin
pinia.use(({ store }) => {
  store.router = markRaw(router);
});

export default pinia;
