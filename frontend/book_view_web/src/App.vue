<template>
  <!--    <bookMainViewIndex />-->
  <!--  <PSImainView/>-->
  <comic-manager/>
</template>

<script>
import PSImainView from "./components/PSImainView.vue";
import bookMainViewIndex from "./components/bookMainViewIndex.vue";
import ComicManager from "@/components/comicManager";

export default {
  name: "App",
  components: {
    ComicManager,
    PSImainView,
    bookMainViewIndex,
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
</style>
