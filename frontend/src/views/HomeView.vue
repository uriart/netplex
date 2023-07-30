<script lang="ts">
  import { defineComponent } from "vue";
  import NavbarView from "./NavbarView.vue";
  import CurrentMovies from "./CurrentMovies.vue";

  export default defineComponent({
    components: {
      NavbarView,
      CurrentMovies,
    }
  });
</script>

<template>
  <main>
    <div className="body">
      <NavbarView/>
    </div>
    <div>
      <CurrentMovies/>
    </div>
  </main>
</template>