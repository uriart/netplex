<template>
  <div>
    <div v-if="loading.value">Cargando...</div>
    <div v-else class="m-5">
      <div class="row row-cols-1 row-cols-md-4 g-4">
        <div class="col" v-for="movie in movies_data" :key="movie.name">
          <div class="card">
            <img :src="movie.image" class="card-img-top" :alt="movie.name">
            <div class="card-body">
              <h5 class="card-title">{{ movie.name }}</h5>
              <button @click="tmp_movie=movie.name" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#exampleModal">Eliminar</button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <!-- Modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">Eliminar</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          Se va a eliminar la película <b>{{ tmp_movie }}</b>. ¿Desea continuar?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
          <button @click="delete_movie(tmp_movie)" type="button" data-bs-dismiss="modal" class="btn btn-primary">Aceptar</button>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script lang="ts">
  import { defineComponent, reactive, onMounted, ref } from 'vue'
  import axios from 'axios';
  
  export default defineComponent({
    setup() {

      const loading = reactive<{ value: boolean }>({ value: true })
      const imdb_uri = 'https://imdb-api.projects.thetuhin.com'
      const backend_python = 'http://localhost:3001'
      const movies_data = reactive<{ name: string; image: string; description: string }[]>([]);
      const tmp_movie = ref('')

      onMounted(getMoviesTitles);

      async function getMoviesTitles() {
        try {
          const response = await axios.get<string[]>(backend_python + "/list_files")
          const names = response.data;
          if (Array.isArray(names)) {
            movies_data.push(...names.map((name) => ({ name, image: '', description: '' })));
            loading.value = false;
            await getMoviesData();
          }
        } catch (error) {
          console.error("Error al obtener la lista de directorios:", error)
        }
      }

      async function getMoviesData() {
        try {
          for (let movie of movies_data) {
            const response = await axios.get<string[]>(imdb_uri + '/search?query=' + movie.name);
            const results = response.data.results;
            if (results.length > 0) {
              movie.image = results[0].image;
              movie.description = results[0].imdb;
            }
          }
        } catch (error) {
          console.error("Error al obtener los datos de las películas:", error)
        }
      }
  
      async function delete_movie(name: string) {
        try {
          console.log("Borrando la película:", name);
          await axios.delete(backend_python + '/delete_directory/' + name);
          const index = movies_data.findIndex(movie => movie.name === name);
          if (index !== -1) {
            movies_data.splice(index, 1);
          }
        } catch (error) {
          console.error("Error al borrar la película:", error)
        }
      }

  
      // Devolvemos las variables que deseamos exponer desde el setup()
      return {
        movies_data,
        loading,
        delete_movie,
        tmp_movie,
      }
    }
  })
</script>
  
<style>
  .card-img {
    width: 400px;
    height: 600px;
  }
</style>