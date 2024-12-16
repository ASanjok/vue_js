<template>
  <b-row align-v="center" class="d-flex flex-wrap align-items-stretch justify-content-start">
    <slotFromComponent class="col-12">
      Anime database
    </slotFromComponent>

    <template v-if="animes.length > 0">
      <b-col v-for="anime in animes" :key="anime.id" cols="12" md="6" lg="4" class="mb-4">

        <div class="anime-item p-3">
          <slotFromComponent>
            <h5>{{ anime.name }}</h5>
          </slotFromComponent>
          <slotFromComponent>
            <p>Episodes: {{ anime.episodeCount }}</p>
          </slotFromComponent>
          <slotFromComponent>
            <p>Status: {{ anime.statusF.name }}</p>
          </slotFromComponent>
          <slotFromComponent>
            <p>Current Episode: {{ anime.onEpisode }}</p>
          </slotFromComponent>
        </div>
      </b-col>
      <b-col cols="12" md="6" lg="4" class="mb-4">
        <div class="anime-item p-3 ">
          <slotFromComponent>
            <b-form-input style="margin-left: -15px; width: 109%;" v-model="animeName"
              placeholder="Enter anime name"></b-form-input>
          </slotFromComponent>
          <slotFromComponent>
            <b-form-input style="margin-left: -15px; width: 109%;" v-model="episodeCount"
              placeholder="Enter episode amount"></b-form-input>
          </slotFromComponent>
          <slotFromComponent style="visibility:hidden;" :style="{ visibility: showMessage ? 'visible' : 'hidden' }">
            enter the values
          </slotFromComponent>
          <slotFromComponent>
            <b-button style="margin-left: -15px;" class="btn-success" @click="submitAnimeData">enter the
              anime</b-button>
          </slotFromComponent>
        </div>
      </b-col>

    </template>

    <template v-else>
      <slotFromComponent>Loading data...</slotFromComponent>
    </template>
  </b-row>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import slotFromComponent from "@/components/slot.vue";

const animes = ref([]);


const fetchAnimes = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/animeList/');
    const data = await response.json();
    animes.value = data;
  } catch (error) {
    console.error('Error:', error);
    alert('There was an error with the GET request');
  }
};

onMounted(() => {
  fetchAnimes();
});

const animeName = ref('')
const episodeCount = ref('')
const showMessage = ref(false)

const submitAnimeData = async () => {
  if (!animeName.value || !episodeCount.value) {
    showMessage.value = true;
    return;
  }

  const animeData = {
    name: animeName.value,
    episodeCount: episodeCount.value
  };

  try {
    const response = await fetch('http://localhost:8000/api/v1/animeList/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(animeData),
    });

    if (response.ok) {      
      animeName.value = '';
      episodeCount.value = '';

    } else {
      alert('Error adding anime');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('There was an error with the POSTrequest');
  }
showMessage.value = false
fetchAnimes();
}


</script>

<style scoped>
.anime-item {
  background-color: #f5f5f5;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
