<template>
  <div data-theme="synthwave" class="bg-musicdibs min-h-screen">
    <Topbar />
    <main class="mx-auto max-w-full pt-20 sm:max-w-screen-lg">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script>
import Topbar from "./components/Topbar.vue";
import Footer from "./components/Footer.vue";

export default {
  components: {
    Topbar,
    Footer,
  },
};
</script>
