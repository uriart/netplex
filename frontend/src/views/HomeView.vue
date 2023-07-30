<script lang="ts">
  import { defineComponent } from "vue";
  import NavbarView from "./NavbarView.vue";

  export default defineComponent({
    components: {
      NavbarView,
    }
  });
</script>

<template>
  <main>
    <div className="body">
      <NavbarView/>
    </div>
  </main>
</template>