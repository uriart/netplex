<template>
    <div>
      <div v-if="loading.value">Cargando...</div>
      <div v-else class="m-5">
        <div class="row row-cols-1 row-cols-md-4 g-4">
            <!--div class="col" v-for="(item, index) in obj_final" :key="index">
                <div class="card" >
                    <img :src="item.image" class="card-img-top" :alt="item.title">
                    <div class="card-body">
                        <h5 class="card-title">{{ item.title }}</h5>
                        <p class="card-text">This is a longer card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                    </div>
                </div>
            </div-->
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, onMounted } from 'vue';
  import axios, { Axios } from 'axios';
  
  export default defineComponent({
    setup() {

      const loading = reactive<{ value: boolean }>({ value: true }); // Inicializar 'loading' como un objeto con propiedad 'value' booleana
      
      async function getListFiles() {
        try {
          // Realizar la solicitud HTTP GET al endpoint de la API utilizando axios
          const movies = await axios.get<string[]>("http://localhost:3001/list_files");
          loading.value = false; // Se ha terminado de cargar, establecemos loading a false
        } catch (error) {
          console.error("Error al obtener la lista de directorios:", error);
        }
      }
  
      // Llamar getListFiles() al cargar la página
      onMounted(getListFiles);
  
      // Devolvemos las variables que deseamos exponer desde el setup()
      return {
        loading,
      };
    },
  });
  </script>
  