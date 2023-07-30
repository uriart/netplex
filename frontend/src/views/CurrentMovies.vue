<template>
    <div>
      <div v-if="loading.value">Cargando...</div>
      <div v-else class="m-5">
        <div class="row row-cols-1 row-cols-md-4 g-4">
            <div class="col" v-for="(item, index) in obj_final" :key="index">
                <div class="card" >
                    <img :src="item.image" class="card-img-top" :alt="item.title">
                    <div class="card-body">
                        <h5 class="card-title">{{ item.title }}</h5>
                        <p class="card-text">This is a longer card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, onMounted } from 'vue';
  import axios from 'axios';
  
  export default defineComponent({
    setup() {
      const directories = reactive<string[]>([]); // Utilizamos el hook 'reactive' para hacer la variable reactiva
      const loading = reactive<{ value: boolean }>({ value: true }); // Inicializar 'loading' como un objeto con propiedad 'value' booleana
      const obj_final:any[] = []
      async function getListFiles() {
        try {
          const config_trakt = {
            headers: {
                'trakt-api-key': '52fee50539768ae2a6a4b6bfb5530e7bbbc178d5a73d15500a6cd755be0135f1',
                // Aquí puedes agregar otros encabezados si es necesario
            },
          };
          const tmdb_apy_key = 'b3dcca2d3ccb476f2e4150f12ac3a8e0';

          // Realizar la solicitud HTTP GET al endpoint de la API utilizando axios
          const movies = await axios.get<string[]>("http://localhost:3001/list_files");
          
          for (const movie of movies.data) {
            const trakt_data = await axios.get<string[]>("https://api.trakt.tv/search/movie?query=" + movie, config_trakt)
            const movie_data = await axios.get<string[]>("https://api.themoviedb.org/3/search/movie?query=" + trakt_data.data[0]?.movie?.ids?.slug + "&api_key=" + tmdb_apy_key)
            
            let movie_image = 'https://image.tmdb.org/t/p/original' + movie_data.data.results[0]?.poster_path
            if (movie_data.data.results[0]?.poster_path == undefined)
                movie_image = 'https://cdn.vectorstock.com/i/preview-1x/65/30/default-image-icon-missing-picture-page-vector-40546530.jpg'

            const tmp = {
                "title": movie,
                "image": movie_image
            }

            obj_final.push(tmp)
          }
          

          console.log(obj_final)
          loading.value = false; // Se ha terminado de cargar, establecemos loading a false
        } catch (error) {
          console.error("Error al obtener la lista de directorios:", error);
        }
      }
  
      // Llamar getListFiles() al cargar la página
      onMounted(getListFiles);
  
      // Devolvemos las variables que deseamos exponer desde el setup()
      return {
        obj_final,
        loading,
      };
    },
  });
  </script>
  