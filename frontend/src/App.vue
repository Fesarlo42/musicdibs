<template>
  <div data-theme="synthwave" class="bg-musicdibs min-h-screen">
    <TopBar />
    <main class="mx-auto max-w-full pt-20 sm:max-w-screen-lg">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script>
import TopBar from "./components/TopBar.vue";
import Footer from "./components/Footer.vue";

export default {
  components: {
    TopBar,
    Footer,
  },
};
</script>
